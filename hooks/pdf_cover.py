"""MkDocs build-time hook: date the manual's front cover from git.

Loaded only by `mkdocs.pdf.yml`; the website build never sees it.

`pdf/cover.html` is the front cover mkdocs-exporter places on the first page of
`adam-manual.pdf`. It has to carry the date the manual was last updated, and it
cannot work that out for itself: `Renderer.cover` reads the template with
`open().read()` and prepends it to the page's Markdown verbatim. Cover
templates are *not* rendered through Jinja, so `{{ ... }}` in one is delivered
to the reader as four braces rather than a value.

This hook substitutes the date instead. The seam is `on_page_markdown`, and the
ordering is what makes it work: mkdocs-exporter's own `on_page_markdown` is
decorated `@event_priority(100)` and a plain hook function runs at the default
0, so by the time this is called the cover markup is already sitting at the top
of the Markdown string, placeholder and all.

The date is the last commit that touched `docs/`, not the build date and not
HEAD. A rebuild is triggered by a CSS or workflow edit as readily as by a
change to the manual, and a cover that re-dates itself when nothing a reader
can see has changed is telling them something untrue. This is the same
reasoning as `hooks/sitemap_lastmod.py`, which exists because MkDocs dates
every sitemap entry from the clock.

`.github/workflows/pdf.yml` checks out with `fetch-depth: 0`, so the history is
present where this actually runs. Where it is not — a shallow clone, an export
with no `.git` — the cover falls back to today's date with a warning, because
no version of a cover date is worth failing a 750-page build over.

The placeholder is an HTML comment on purpose. If this hook is ever dropped
from `mkdocs.pdf.yml` (which replaces the `hooks` list rather than merging it,
so a hook can go missing by omission elsewhere) the cover loses its date
silently rather than printing markup at the reader.
"""

import datetime
import logging
import subprocess

log = logging.getLogger('mkdocs.hooks.pdf_cover')

PLACEHOLDER = '<!--cover-date-->'

GIT_TIMEOUT_SECONDS = 30


def _last_docs_commit_date(docs_dir):
    """Return the date of the last commit touching docs/, or None.

    `%cs` is git's committer date as a bare YYYY-MM-DD, so nothing here has to
    parse a timestamp or reason about time zones.

    The catch is deliberately broad, and on the same evidence as the one in
    `hooks/sitemap_lastmod.py`: a narrow tuple that misses one failure class
    fails the build it promised not to.
    """
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%cs', '--', str(docs_dir)],
            cwd=str(docs_dir),
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
            check=True,
        )
    except Exception as exc:  # noqa: BLE001 - see the docstring
        log.warning('pdf_cover: git unavailable (%s); dating the cover from the clock.', exc)
        return None

    return result.stdout.strip() or None


def _format(iso_date):
    """Render YYYY-MM-DD as `16 September 2026`.

    `%-d` drops the leading zero, which `%d` would keep: "06 September" reads
    like a part number. It is a GNU extension rather than C89, which is safe
    here — the manual is built on Ubuntu runners and Linux servers — but is the
    reason this is not simply `strftime('%-d %B %Y')` everywhere.
    """
    return datetime.date.fromisoformat(iso_date).strftime('%-d %B %Y')


# Resolved once per build rather than once per page: 100 pages carry the cover
# markup, and only the first survives into the manual, but each is preprocessed.
_date = None


def on_config(config, **kwargs):
    """Works out the cover date before any page is rendered."""

    global _date

    iso_date = _last_docs_commit_date(config['docs_dir'])

    if iso_date is None:
        _date = _format(datetime.date.today().isoformat())
    else:
        _date = _format(iso_date)
        log.info('pdf_cover: manual last updated %s.', _date)

    return config


def on_page_markdown(markdown, **kwargs):
    """Fills in the cover's date placeholder."""

    if PLACEHOLDER not in markdown:
        return markdown

    return markdown.replace(PLACEHOLDER, _date)
