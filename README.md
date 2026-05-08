# ADAM User Documentation

End-user documentation for ADAM (Academic Data Manager), authored as Markdown and built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Local development

### Option A: Python venv

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

The site is served at `http://127.0.0.1:8000` and live-reloads on change.

### Option B: Docker (no Python install required)

```bash
docker run --rm -it --user "$(id -u):$(id -g)" \
    -p 8000:8000 -v "$(pwd):/docs" -w /docs \
    squidfunk/mkdocs-material:latest serve --dev-addr=0.0.0.0:8000
```

Replace `serve --dev-addr=0.0.0.0:8000` with `build --strict` to produce a static site under `site/`.

## Authoring conventions

- One Markdown file per top-level chapter, lower-kebab-case filenames under `docs/`.
- UI labels are in **bold**.
- Menu paths are written as natural prose: "click on the **Administration tab**, then under the **Absentee Administration heading**, click on **Edit the absentee reasons**."
- Screenshots live under `docs/assets/screenshots/<chapter-slug>/` and are referenced with relative paths.

## Screenshots

Screenshots are captured against a demo school tenant, never against production. The capture workflow is documented in [`scripts/README.md`](scripts/README.md) (forthcoming).

## History

This site replaces a fragile pipeline that consumed a Google Doc published as HTML. The initial Markdown corpus was converted from that source by `scripts/convert_html_to_markdown.py`.
