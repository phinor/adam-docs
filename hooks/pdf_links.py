"""MkDocs build-time hook: stop the PDF exporter mangling `mailto:` links.

Loaded only by `mkdocs.pdf.yml`; the website build never sees it.

A PDF has no page it sits on, so relative links in it cannot resolve. The
exporter rewrites them against `site_url`, which is what makes cross-references
work on paper. Its test for "already absolute" is `urlparse(href).netloc`
(`mkdocs_exporter/formats/pdf/preprocessor.py`), and that is the bug: a
`mailto:` URL has a scheme but no netloc, and a non-empty path, so it passes
both guards and is rewritten like a page link. Every address in the manual
turns into `https://help.adam.co.za/help@adam.co.za` — 13 of them, and not one
working `mailto:` left.

Checking the scheme as well as the netloc fixes it, and covers `tel:` and any
other scheme-only link the manual grows later.

This patches the exporter's own method because the rewrite runs *after* the
theme adapter has had the DOM, so there is no earlier seam to correct it from.
"""

import logging

from urllib.parse import urljoin, urlparse

from mkdocs_exporter.formats.pdf.preprocessor import Preprocessor

log = logging.getLogger('mkdocs.hooks.pdf_links')


def rewrite_links(self, base, root):
    """Rewrites relative links against the site URL, leaving other schemes be."""

    final = urlparse(root)

    for element in self.html.find_all('a', href=True):
        url = urlparse(element['href'])

        if url.scheme or url.netloc:
            # http(s), mailto, tel — already absolute, or not a page at all.
            continue
        if not url.path:
            # A bare `#anchor`, which stays within the document.
            continue

        element['href'] = url._replace(
            netloc=final.netloc,
            scheme=final.scheme,
            path=urljoin(base, url.path),
        ).geturl()


Preprocessor.rewrite_links = rewrite_links
