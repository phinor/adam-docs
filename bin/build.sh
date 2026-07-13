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
# STRICT defaults on for local --dev builds, off for unattended deploys.
if [[ -n "${STRICT:-}" ]]; then STRICT="$STRICT"; elif [[ "$DEV" == "1" ]]; then STRICT=1; else STRICT=0; fi

log () { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

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
