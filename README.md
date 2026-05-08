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

## Deployment

The site is self-hosted at `https://help.adam.co.za/`, served as static files by the same web server that hosts ADAM. The deployment server runs `bin/build.sh` from a cron, which:

1. fetches the latest commit on `main`,
2. builds the site via the `squidfunk/mkdocs-material` Docker image,
3. atomically swaps the freshly-built `site/` into the path the web server reads from.

If `main` has not advanced since the last build, the script exits without rebuilding.

### One-time server setup

```bash
# Clone alongside any existing checkouts
git clone git@github.com:phinor/adam-docs.git /opt/adam-docs

# Pre-pull the build image so the first cron run isn't slow
docker pull squidfunk/mkdocs-material:latest

# Point the web server at the build output. Either:
#   (a) leave PUBLISH_DIR empty so the site is built in /opt/adam-docs/site/,
#       and configure the vhost root to that path, or
#   (b) export PUBLISH_DIR to wherever the existing vhost already serves from
#       (e.g. /var/www/help.adam.co.za) so no nginx/Apache changes are needed.
```

### Cron entry

Every five minutes is generally fine — the no-op path is cheap.

```cron
*/5 * * * * PUBLISH_DIR=/var/www/help.adam.co.za /opt/adam-docs/bin/build.sh >> /var/log/adam-docs.log 2>&1
```

Set `FORCE_PULL=1` once a week (or in a separate weekly entry) if you want the script to refresh the MkDocs Docker image.

### Switching from the legacy pipeline

The old `adam-documentation` PHP project deployed to the same `help.adam.co.za` vhost. To cut over:

1. Disable its cron (`generate.php`).
2. Run `bin/build.sh` once on the server with `PUBLISH_DIR` pointing at the existing vhost root — the old HTML is replaced with the MkDocs build.
3. Verify the site loads, then enable the new cron entry.

The legacy repo can stay checked out as a fallback until the new site is validated.

## History

This site replaces a fragile pipeline that consumed a Google Doc published as HTML. The initial Markdown corpus was converted from that source by `scripts/convert.mjs`.
