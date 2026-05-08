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
#
# Exit codes:
#   0  build succeeded (or no new commits to deploy)
#   1  git fetch / pull failed
#   2  mkdocs build failed
#   3  publish swap failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="${REPO_DIR:-$(dirname "$SCRIPT_DIR")}"
PUBLISH_DIR="${PUBLISH_DIR:-$REPO_DIR/site}"
GIT_BRANCH="${GIT_BRANCH:-main}"
MKDOCS_IMAGE="${MKDOCS_IMAGE:-squidfunk/mkdocs-material:latest}"
FORCE_PULL="${FORCE_PULL:-0}"

log () { printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"; }

cd "$REPO_DIR"

log "Fetching $GIT_BRANCH"
git fetch --quiet origin "$GIT_BRANCH" || { log "git fetch failed"; exit 1; }

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse "origin/$GIT_BRANCH")

if [[ "$LOCAL" == "$REMOTE" ]] && [[ -d "$PUBLISH_DIR" ]] && [[ -n "$(ls -A "$PUBLISH_DIR" 2>/dev/null)" ]]; then
    log "Already up-to-date at $LOCAL; nothing to do"
    exit 0
fi

log "Updating working tree from $LOCAL to $REMOTE"
git reset --hard "origin/$GIT_BRANCH"

if [[ "$FORCE_PULL" == "1" ]]; then
    log "Pulling latest $MKDOCS_IMAGE"
    docker pull --quiet "$MKDOCS_IMAGE"
fi

# Build into a staging directory inside the repo, then atomically swap.
STAGE_DIR="$REPO_DIR/.build-staging"
rm -rf "$STAGE_DIR"

log "Building site"
docker run --rm \
    --user "$(id -u):$(id -g)" \
    -v "$REPO_DIR:/docs" \
    -w /docs \
    "$MKDOCS_IMAGE" \
    build --strict --site-dir /docs/.build-staging \
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

log "Deployed $REMOTE to $PUBLISH_DIR"
