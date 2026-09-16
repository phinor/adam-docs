"""MkDocs build-time hook: render GitHub alerts as admonitions.

Turns

    > [!WARNING]
    > Body text.

into the same `<div class="admonition warning">` that Python-Markdown's
`admonition` extension produces for `!!! warning`, so `theme/css/styles.css`
needs no changes. The alert syntax is used instead of `!!!` because editors
parse it -- it is a plain blockquote to anything that does not know the
extension, rather than a paragraph that swallows the lines beneath it.

Vendored from `markdown-callouts` (MIT, Oleh Prypin) rather than installed,
because `bin/build.sh` deploys through the `squidfunk/mkdocs-material` image,
which has no pip step and does not carry the package. A hook is loaded by
file path, so it works in that image, in the PDF build and in a local venv
without anything being installed. See the same reasoning in `mkdocs.pdf.yml`
for why mkdocs-exporter is kept out of the main config.

Registered as an extension *instance* rather than a name: MkDocs hands
`config['markdown_extensions']` straight to `markdown.Markdown(extensions=)`
(mkdocs/structure/pages.py), which accepts instances, and an instance needs
no import path -- which this file, not being an installed module, does not
have.
"""

import re
import xml.etree.ElementTree as etree

from markdown import util
from markdown.blockprocessors import BlockQuoteProcessor
from markdown.extensions import Extension

# GitHub defines five alert types; this theme styles four admonition classes.
# `caution` and `important` have no rule of their own, so they borrow the two
# that carry the same weight. (Upstream maps only caution; important -> info
# is this site's own choice.)
CLASSES = {
    'note': 'note',
    'tip': 'tip',
    'important': 'info',
    'warning': 'warning',
    'caution': 'danger',
}


class _GitHubCalloutsBlockProcessor(BlockQuoteProcessor):
    # Group 1 is whatever precedes the alert in the same block and is parsed
    # separately; group 3 marks where the body starts. Kept as upstream wrote
    # it -- the leading context is what stops a `[!NOTE]` partway down a real
    # blockquote from being promoted.
    REGEX = re.compile(
        r'((?:^|\n) *(?:[^>].*)?(?:^|\n)) {0,3}> *\[!'
        r'(NOTE|TIP|IMPORTANT|WARNING|CAUTION)'
        r'\] *\n(?: *> *\n)*() *(?:> *[^\s\n]|[^\s\n>])',
        flags=re.IGNORECASE,
    )

    def test(self, parent, block):
        return (
            bool(self.REGEX.search(block))
            and not self.parser.state.isstate('blockquote')
            and not util.nearing_recursion_limit()
        )

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.REGEX.search(block)

        before = block[:m.end(1)]
        body = '\n'.join(self.clean(line) for line in block[m.end(3):].split('\n'))
        self.parser.parseBlocks(parent, [before])

        kind = m[2].lower()
        admon = etree.SubElement(
            parent, 'div', {'class': 'admonition ' + CLASSES[kind]}
        )
        title = etree.SubElement(admon, 'p', {'class': 'admonition-title'})
        title.text = kind.title()

        # Guards against a nested alert: the blockquote state makes `test`
        # decline, so the inner one stays an ordinary blockquote.
        self.parser.state.set('blockquote')
        self.parser.parseChunk(admon, body)
        self.parser.state.reset()


class GitHubCalloutsExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(
            _GitHubCalloutsBlockProcessor(md.parser),
            'github-callouts',
            21.1,  # Just above 'quote' (20), so alerts are claimed first.
        )


def on_config(config, **kwargs):
    config['markdown_extensions'].append(GitHubCalloutsExtension())
    return config
