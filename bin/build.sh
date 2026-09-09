#!/usr/bin/env bash
#
# Build the documentation site on the deployment server.
#
# Pulls the latest from git, runs `mkdocs build` (via Docker), and atomically
# swaps the result into place so partial builds are never served. Designed to
# be run on a cron schedule:
#
#   */5 * * * * /path/to/adam-docs/bin/build.sh >> /var/log/adam-docs.log 2>&1
#
# Configuration via environment variables (with sensible defaults):
#
#   REPO_DIR       Path to the adam-docs checkout. Default: directory above this script.
#   PUBLISH_DIR    Path the web server reads from. Default: $REPO_DIR/site.
#                  May be the same as $REPO_DIR/site or somewhere outside the repo.
#   GIT_BRANCH     Branch to deploy. Default: main.
#   MKDOCS_IMAGE   Docker image to build with. Default: squidfunk/mkdocs-material:latest.
#   FORCE_PULL     If "1", always pull the latest image before building. Default: 0.
#   PDF_URL        Where the downloadable manual is published by CI. The site
#                  links to /adam-manual.pdf; this is where that file comes from.
#                  Default: the manual-pdf release asset in phinor/adam-docs.
#   PDF_CACHE      Local copy of that PDF, kept across runs so an unchanged
#                  manual is not re-downloaded. Its ETag is remembered beside it
#                  in <PDF_CACHE>.id, and each run downloads only when the two
#                  differ. Default: $REPO_DIR/.pdf-cache/adam-manual.pdf.
#   SKIP_PDF       If "1", publish the site without the PDF. Default: 0.
#   STRICT         If "1", build with --strict so warnings (e.g. broken links)
#                  abort the build. Default: 0 for deploys (so a single broken
#                  link can't freeze the whole site), 1 in --dev mode (to catch
#                  issues before they ship). Set explicitly to override either.
#
# Options:
#   --force, -f    Rebuild even if the checkout is already up-to-date with the
#                  remote. Normally a deploy run exits early when there are no
#                  new commits and the site is already published; --force skips
#                  that check. Useful after changing the theme, this script, or
#                  the Docker image without a new content commit, or to seed a
#                  fresh server. (Env: FORCE_BUILD=1. No effect with --dev, which
#                  always builds.)
#   --dev          Local build: skip all git operations (fetch/reset) and build
#                  the working tree exactly as it is on disk. Still builds via
#                  the staging dir and atomically swaps into PUBLISH_DIR (default
#                  $REPO_DIR/site), and defaults STRICT=1. Use this to inspect
#                  the generated site/ without pulling. For a live-reloading
#                  preview, `mkdocs serve` is nicer (see README).
#
# Exit codes:
#   0  build succeeded (or no new commits to deploy)
#   1  git fetch / pull failed
#   2  mkdocs build failed
#   3  publish swap failed

set -euo pipefail

DEV=0
FORCE_BUILD="${FORCE_BUILD:-0}"
for arg in "$@"; do
    case "$arg" in
        --dev) DEV=1 ;;
        --force|-f) FORCE_BUILD=1 ;;
        -h|--help) sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) printf 'unknown argument: %s\n' "$arg" >&2; exit 64 ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${REPO_DIR:-$(dirname "$SCRIPT_DIR")}"
PUBLISH_DIR="${PUBLISH_DIR:-$REPO_DIR/site}"
GIT_BRANCH="${GIT_BRANCH:-main}"
MKDOCS_IMAGE="${MKDOCS_IMAGE:-squidfunk/mkdocs-material:latest}"
FORCE_PULL="${FORCE_PULL:-0}"
PDF_URL="${PDF_URL:-https://github.com/phinor/adam-docs/releases/download/manual-pdf/adam-manual.pdf}"
PDF_CACHE="${PDF_CACHE:-$REPO_DIR/.pdf-cache/adam-manual.pdf}"
SKIP_PDF="${SKIP_PDF:-0}"
# STRICT defaults on for local --dev builds, off for unattended deploys.
if [[ -n "${STRICT:-}" ]]; then STRICT="$STRICT"; elif [[ "$DEV" == "1" ]]; then STRICT=1; else STRICT=0; fi

log () { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

# The downloadable manual, kept current on the server.
#
# The PDF is built by .github/workflows/pdf.yml, not here: it needs a headless
# Chromium the mkdocs image does not carry, and this script runs every five
# minutes.
#
# That workflow finishes two to four minutes *after* the commit that triggered
# it, so the deploy reacting to that commit is always too early to collect the
# matching PDF. The manual therefore cannot be tied to the site build: it is
# synced on every run, including the runs that find nothing to deploy.
#
# Syncing every run is not the same as downloading every run. Each run asks the
# server for the asset's ETag — one small request — and downloads the 40 MB only
# when that differs from the copy already cached. In steady state a five-minute
# cron costs a few hundred bytes a tick, and the transfer happens once per
# published manual.
#
# None of it is fatal. A missing or unreachable PDF costs a dead download link
# on the home page; failing the deploy over it would take the whole site down.

# Identifier for the currently published asset: its ETag, or its Last-Modified
# if the server offers no ETag. Empty if neither could be read, which callers
# treat as "unknown" rather than as "unchanged".
pdf_remote_id () {
    local headers

    # --head follows the redirect to the asset host and prints the headers of
    # every hop, so the last value seen is the one describing the file itself.
    headers="$(curl --fail --location --silent --show-error --head \
                    --max-time 30 "$PDF_URL" 2>/dev/null || true)"

    # `|| true` is load-bearing: with `set -euo pipefail`, grep finding no
    # match makes the pipeline — and so the command substitution that calls
    # this — non-zero, which would abort the entire deploy because a header
    # was missing.
    printf '%s' "$headers" \
        | tr -d '\r' \
        | grep -iE '^(etag|last-modified):' \
        | tail -1 \
        | cut -d' ' -f2- \
        | tr -d '"' \
        || true
}

# Refresh the cached copy if what is published differs from it.
refresh_pdf_cache () {
    local remote_id cached_id

    mkdir -p "$(dirname "$PDF_CACHE")"

    remote_id="$(pdf_remote_id)"
    cached_id="$(cat "$PDF_CACHE.id" 2>/dev/null || true)"

    if [[ -n "$remote_id" && -f "$PDF_CACHE" && "$remote_id" == "$cached_id" ]]; then
        return 0
    fi

    # --time-cond is a second line of defence for a server that returned no
    # ETag: a 304 writes no body, which is why an empty result is discarded
    # rather than published.
    if ! curl --fail --location --silent --show-error \
              --max-time 600 --retry 2 \
              --time-cond "$PDF_CACHE" \
              --output "$PDF_CACHE.tmp" \
              "$PDF_URL"; then
        rm -f "$PDF_CACHE.tmp"
        log "WARNING: could not fetch manual PDF from $PDF_URL"

        return 0
    fi

    if [[ ! -s "$PDF_CACHE.tmp" ]]; then
        rm -f "$PDF_CACHE.tmp"

        return 0
    fi

    # An error page or a captive-portal login served with a 200 would otherwise
    # be published as the manual.
    if [[ "$(head -c 4 "$PDF_CACHE.tmp")" != "%PDF" ]]; then
        rm -f "$PDF_CACHE.tmp"
        log "WARNING: download from $PDF_URL is not a PDF; keeping previous copy"

        return 0
    fi

    mv "$PDF_CACHE.tmp" "$PDF_CACHE"
    printf '%s' "$remote_id" > "$PDF_CACHE.id"
    log "Fetched updated manual PDF ($(du -h "$PDF_CACHE" | cut -f1))"

    return 0
}

# Place the cached manual into a directory that is about to become the site.
install_pdf () {
    local target="$1"

    if [[ ! -f "$PDF_CACHE" ]]; then
        log "WARNING: no manual PDF to publish; /adam-manual.pdf will 404"

        return 0
    fi

    # Written beside the destination and renamed, so a reader mid-download
    # never sees a half-copied file. Same filesystem, so the rename is atomic.
    cp "$PDF_CACHE" "$target/adam-manual.pdf.tmp"
    mv "$target/adam-manual.pdf.tmp" "$target/adam-manual.pdf"

    return 0
}

# Sync the manual into an already-published site, for runs with nothing to
# deploy. This is the path that actually picks up a newly built PDF, since the
# workflow always finishes after the deploy that triggered it.
sync_published_pdf () {
    if [[ "$SKIP_PDF" == "1" ]]; then
        return 0
    fi

    refresh_pdf_cache

    if [[ -f "$PDF_CACHE" ]] && ! cmp --silent "$PDF_CACHE" "$PUBLISH_DIR/adam-manual.pdf" 2>/dev/null; then
        install_pdf "$PUBLISH_DIR"
        log "Published updated manual PDF to $PUBLISH_DIR"
    fi

    return 0
}

# Collect the manual into the staging directory, so it is swapped into place
# with the rest of the site rather than appearing separately.
collect_pdf () {
    if [[ "$SKIP_PDF" == "1" ]]; then
        log "Skipping PDF (SKIP_PDF=1)"

        return 0
    fi

    refresh_pdf_cache
    install_pdf "$STAGE_DIR"

    return 0
}

cd "$REPO_DIR"

if [[ "$DEV" == "1" ]]; then
    SOURCE="working tree ($(git rev-parse --short HEAD 2>/dev/null || echo 'no git'))"
    log "Dev build: skipping git; building working tree as-is"
else
    SOURCE="origin/$GIT_BRANCH"

    log "Fetching $GIT_BRANCH"
    git fetch --quiet origin "$GIT_BRANCH" || { log "git fetch failed"; exit 1; }

    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse "origin/$GIT_BRANCH")

    if [[ "$FORCE_BUILD" != "1" ]] \
        && [[ "$LOCAL" == "$REMOTE" ]] \
        && [[ -d "$PUBLISH_DIR" ]] \
        && [[ -n "$(ls -A "$PUBLISH_DIR" 2>/dev/null)" ]]; then
        # Nothing to deploy, but the manual is built after the commit that
        # triggers it, so this is the run that collects it. Costs one small
        # request unless the published PDF has actually changed.
        sync_published_pdf
        log "Already up-to-date at $LOCAL; nothing to do"
        exit 0
    fi
    [[ "$FORCE_BUILD" == "1" ]] && log "Force build requested; rebuilding even if up-to-date"

    log "Updating working tree from $LOCAL to $REMOTE"
    git reset --hard "origin/$GIT_BRANCH"
fi

if [[ "$FORCE_PULL" == "1" ]]; then
    log "Pulling latest $MKDOCS_IMAGE"
    docker pull --quiet "$MKDOCS_IMAGE"
fi

# Build into a staging directory inside the repo, then atomically swap.
STAGE_DIR="$REPO_DIR/.build-staging"
rm -rf "$STAGE_DIR"

STRICT_FLAG=()
if [[ "$STRICT" == "1" ]]; then
    STRICT_FLAG=(--strict)
fi

log "Building site${STRICT:+ (strict=$STRICT)}"
docker run --rm \
    --user "$(id -u):$(id -g)" \
    -v "$REPO_DIR:/docs" \
    -w /docs \
    "$MKDOCS_IMAGE" \
    build "${STRICT_FLAG[@]}" --site-dir /docs/.build-staging \
    || { log "mkdocs build failed"; rm -rf "$STAGE_DIR"; exit 2; }

collect_pdf

# Swap into place.
PUBLISH_PARENT="$(dirname "$PUBLISH_DIR")"
mkdir -p "$PUBLISH_PARENT"

OLD_DIR="${PUBLISH_DIR}.old"
rm -rf "$OLD_DIR"

if [[ -d "$PUBLISH_DIR" ]]; then
    mv "$PUBLISH_DIR" "$OLD_DIR" || { log "could not move $PUBLISH_DIR aside"; exit 3; }
fi
mv "$STAGE_DIR" "$PUBLISH_DIR" || {
    log "could not move staging into place; restoring previous"
    [[ -d "$OLD_DIR" ]] && mv "$OLD_DIR" "$PUBLISH_DIR"
    exit 3
}
rm -rf "$OLD_DIR"

log "Deployed $SOURCE to $PUBLISH_DIR"
