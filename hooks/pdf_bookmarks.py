"""MkDocs build-time hook: give the aggregated PDF a chapter outline.

Loaded only by `mkdocs.pdf.yml`; the website build never sees it.

mkdocs-exporter's aggregator is a plain `PdfWriter.append()` loop and emits no
outline of any kind, so the manual opens with an empty bookmarks pane. At ~750
pages that leaves a reader no way to reach a chapter except scrolling.

Where each chapter starts is only knowable while the aggregate is being
assembled — the per-chapter PDFs are re-rendered for the aggregate and deleted
straight afterwards, so counting the standalone files would be an assumption
rather than a measurement. Each offset is therefore recorded as its chapter is
appended, and the outline written just before the document is saved.

`Aggregator.save()` is wrapped rather than replaced: it also stamps the PDF
metadata, and the outline has to be added to the same writer before that runs.
"""

import logging

from mkdocs_exporter.formats.pdf.aggregator import Aggregator

log = logging.getLogger('mkdocs.hooks.pdf_bookmarks')

_open = Aggregator.open
_append = Aggregator.append
_save = Aggregator.save


def open(self, path):
    """Starts a fresh set of chapter offsets."""

    self.offsets = []

    return _open(self, path)


def append(self, document):
    """Records where this chapter begins, before it is appended."""

    self.offsets.append(len(self.writer.pages))

    return _append(self, document)


def save(self, metadata={}):
    """Writes the chapter outline, then saves."""

    offsets = getattr(self, 'offsets', [])

    for page, offset in zip(self.pages, offsets):
        # `title` is the nav label; the source path is a legible last resort
        # for a page that somehow reaches here without one.
        title = getattr(page, 'title', None) or page.file.src_path

        self.writer.add_outline_item(str(title), offset)

    log.info('pdf_bookmarks: wrote %d chapter bookmarks.', len(offsets))

    return _save(self, metadata)


Aggregator.open = open
Aggregator.append = append
Aggregator.save = save
