"""MkDocs build-time hook: keep the manual's cross-references inside the PDF.

Loaded only by `mkdocs.pdf.yml`; the website build never sees it.

A PDF has no page it sits on, so mkdocs-exporter rewrites every relative link
against `site_url` before rendering — `grades.html#settings` becomes
`https://help.adam.co.za/grades.html#settings`, and Chrome prints that as a
link out to the website. A reader with the manual open is sent to the browser
for a chapter they already have in front of them, and the 1025 cross-references
in `docs/` are all like this.

The rewrite itself is not the problem: it is what makes the links work at all,
and `hooks/pdf_links.py` depends on it. What is missing is the last step, which
mkdocs-exporter has no way to take on its own — a page is rendered long before
anything knows where it lands in the aggregate. So the links are corrected once
the aggregate exists, in the same place `hooks/pdf_bookmarks.py` works.

Two things make that possible:

**Chrome writes a named destination for every `<a href="#id">` in a document**,
and does so even when the link is `display: none` — no visible mark, no
clickable box, just the destination. `hooks/pdf_theme.py` injects one such link
per heading (`permalink: false`, so the pages carry no anchors of their own),
which gives every heading a destination in its chapter's PDF.

**Each chapter's destinations are read before it is merged.** They cannot be
read afterwards: pypdf keeps one entry per name when it appends, and 30 heading
slugs in the manual are repeated across chapters, so the merged table is
missing most of them and wrong about the rest. Reading each chapter separately
also fixes a bug that predates this hook — a same-page anchor link to a
repeated slug currently jumps to whichever chapter was appended last.

Every link that resolves is then rewritten as an explicit destination: a page
of the manual and a point on it, with no name to be shadowed and no URL to
follow. Links that do not resolve — other websites, `mailto:`, images, the one
reference to the site's own home page — are left exactly as they are.
"""

import logging

from collections import namedtuple
from urllib.parse import unquote, urlparse

from pypdf import PdfReader
from pypdf.generic import ArrayObject, FloatObject, NameObject, NullObject

from mkdocs_exporter.formats.pdf.aggregator import Aggregator

log = logging.getLogger('mkdocs.hooks.pdf_internal_links')

# The site the exporter rewrites relative links against. Set from the config,
# because the aggregator is handed documents and nothing else.
site_url = None

# One rendered chapter, in the order it was appended to the manual. `offset` is
# the page of the manual it starts on; `dests` maps a destination name to a
# `Dest` whose page is relative to that offset.
Chapter = namedtuple('Chapter', 'url offset dests')

# Where a link lands: a page, and a point on it. `left` and `top` are `None`
# for the top of the page, which is where a link without a usable anchor goes.
Dest = namedtuple('Dest', 'page left top')


def on_config(config):
    """Records the site URL, which is what links have been rewritten against."""

    global site_url

    site_url = config['site_url']

    if not site_url:
        log.warning('pdf_internal_links: no site_url; cross-references will stay web links.')

    return config


def normalise(name):
    """Returns a destination name in the form a link fragment is looked up by.

    Chrome names a destination after the fragment that reached it, leading
    slash and all, and percent-encodes what a URL would percent-encode.
    """

    return unquote(str(name).lstrip('/'))


def number(value):
    """Returns a coordinate as a float, or `None` where the PDF gives none."""

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def read_destinations(path):
    """Reads what a rendered chapter offers to link to."""

    reader = PdfReader(path)
    dests = {}

    for name, destination in reader.named_destinations.items():
        try:
            page = reader.get_destination_page_number(destination)
        except Exception:
            # A destination pointing at a page this document does not hold.
            continue

        dests[normalise(name)] = Dest(page, number(destination.left), number(destination.top))

    return dests


def chapter_at(chapters, page):
    """Returns the chapter a page of the manual belongs to."""

    found = None

    for chapter in chapters:
        if chapter.offset > page:
            break

        found = chapter

    return found


def resolve_named(chapter, name):
    """Returns where a destination name in a chapter lands in the manual."""

    dest = chapter.dests.get(normalise(name))

    if dest is None:
        return None

    return dest._replace(page=chapter.offset + dest.page)


def resolve_url(chapters, url, root):
    """Returns where a site URL lands in the manual, or `None` for a web link."""

    target = urlparse(url)
    site = urlparse(root)

    if (target.scheme, target.netloc) != (site.scheme, site.netloc):
        return None

    path = unquote(target.path).lstrip('/')

    for chapter in chapters:
        if chapter.url != path:
            continue

        # A heading, or the chapter itself when the anchor is missing — which
        # is what a link to a page with no fragment asks for anyway.
        return resolve_named(chapter, target.fragment) or Dest(chapter.offset, None, None)

    return None


def target(annotation, chapters, chapter, root):
    """Returns where a link annotation should point in the manual, or `None`."""

    dest = annotation.get('/Dest')

    if dest is not None:
        if isinstance(dest, ArrayObject):
            # Already a place in this document.
            return None

        # A name, written by Chrome for a link within the chapter, and resolved
        # against that chapter alone: the merged document's table of names has
        # lost every collision between chapters.
        return resolve_named(chapter, dest) if chapter else None

    action = annotation.get('/A')

    if action is None or action.get_object().get('/S') != '/URI':
        return None

    return resolve_url(chapters, str(action.get_object().get('/URI', '')), root)


def place(writer, annotation, dest):
    """Points a link annotation at a place in the manual."""

    page = writer.pages[dest.page]
    left = dest.left if dest.left is not None else 0.0
    top = dest.top if dest.top is not None else float(page.mediabox.top)

    if '/A' in annotation:
        del annotation[NameObject('/A')]

    annotation[NameObject('/Dest')] = ArrayObject([
        page.indirect_reference,
        NameObject('/XYZ'),
        FloatObject(left),
        FloatObject(top),
        # Null zoom: the reader keeps whatever magnification it is showing,
        # rather than jumping to a fitted view of the target page.
        NullObject(),
    ])


def retarget(writer, chapters, root):
    """Turns every link into the manual into a link within it.

    Returns how many were rewritten. The rest — other websites, `mailto:`
    addresses, and anything on the site that is not a chapter — are left alone.
    """

    count = 0

    for index, page in enumerate(writer.pages):
        chapter = chapter_at(chapters, index)

        for annotation in page.get('/Annots') or []:
            annotation = annotation.get_object()

            if annotation.get('/Subtype') != '/Link':
                continue

            dest = target(annotation, chapters, chapter, root)

            if dest is None:
                continue

            place(writer, annotation, dest)

            count += 1

    return count


_open = Aggregator.open
_append = Aggregator.append
_save = Aggregator.save


def open(self, path):
    """Starts a fresh set of chapters."""

    self.chapters = []

    return _open(self, path)


def append(self, document):
    """Records where this chapter begins and what it offers to link to.

    Both have to be measured here. The offset is only knowable while the
    aggregate is being assembled, and the destinations are only complete before
    the merge, which discards every name a later chapter repeats.
    """

    page = self.pages[len(self.chapters)] if len(self.chapters) < len(self.pages) else None

    self.chapters.append(Chapter(
        url=unquote(page.url) if page else '',
        offset=len(self.writer.pages),
        dests=read_destinations(document),
    ))

    return _append(self, document)


def save(self, metadata={}):
    """Rewrites the links into the manual, then saves."""

    count = retarget(self.writer, getattr(self, 'chapters', []), site_url or '')

    log.info('pdf_internal_links: made %d links internal.', count)

    return _save(self, metadata)


Aggregator.open = open
Aggregator.append = append
Aggregator.save = save
