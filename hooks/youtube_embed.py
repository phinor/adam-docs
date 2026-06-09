"""MkDocs build-time hook: turn raw YouTube links into embedded players.

Any line in a page's Markdown that contains a YouTube link is replaced
wholesale by a block-level <iframe>, without mutating the source files --
the transformation happens in memory during `mkdocs build`.

Recognised link forms:
    https://youtu.be/CODE
    https://www.youtube.com/watch?v=CODE
    https://www.youtube.com/watch?v%3DCODE   (URL-encoded "=")
    https://www.youtube.com/embed/CODE       (defensive; sources are
                                              normalised to watch?v= form)
"""

import re

YT_RE = re.compile(
    r'https?://(?:www\.)?youtu(?:be\.com|\.be)/'
    r'(?:watch\?v=|watch\?v%3[dD]|embed/)?'
    r'([A-Za-z0-9_\-]+)'
)


def _embed(video_id):
    return (
        f'<div class="video-embed"><iframe '
        f'src="https://www.youtube.com/embed/{video_id}" frameborder="0" '
        f'allow="accelerometer; autoplay; encrypted-media; gyroscope; '
        f'picture-in-picture" allowfullscreen></iframe></div>'
    )


def on_page_markdown(markdown, **kwargs):
    out = []
    for line in markdown.split('\n'):
        # Markdown-escaped chars (e.g. `\_`) would otherwise truncate the
        # YouTube ID match. Strip backslash escapes before matching.
        unescaped = re.sub(r'\\([_*\[\]])', r'\1', line)
        m = YT_RE.search(unescaped)
        out.append(_embed(m.group(1)) if m else line)
    return '\n'.join(out)
