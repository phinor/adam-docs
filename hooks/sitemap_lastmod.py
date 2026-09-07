"""MkDocs build-time hook: date every sitemap URL from git, not from the clock.

MkDocs sets `Page.update_date` to the *build* date (`get_build_date()`, in
`mkdocs/structure/pages.py`), and that value is what the built-in sitemap
template emits as `<lastmod>`. `bin/build.sh` rebuilds whenever a commit lands,
so without this hook a one-word fix to a single page re-dates all 99 URLs to
that day. A `lastmod` that behaves like that carries no information, and search
engines discount the ones that do.

Each page is dated instead from the last commit that touched its own Markdown
source, which this repository already knows and nobody has to maintain.

`on_env` is the seam, and it is the only one that works. MkDocs writes
`sitemap.xml` from `config.theme.static_templates` *before* it builds any page
(see the ordering in `mkdocs/commands/build.py`), so a hook on `on_page_context`
would set a date nothing ever reads.

Requires `site_url` in mkdocs.yml. Without it the sitemap template's own guard,
`{% if not file.page.is_link and (file.page.abs_url or file.page.canonical_url) %}`,
is false for every page and the build emits an empty `<urlset>`: there would be
no URLs here to date.

Any file git cannot date keeps MkDocs' build date, so a shallow clone, an export
with no `.git`, or a page added and not yet committed all degrade to today's
behaviour rather than failing the build.
"""

import logging
import subprocess
from pathlib import Path

log = logging.getLogger('mkdocs.hooks.sitemap_lastmod')

# Separates commits in the `git log` stream. A NUL cannot occur in a path, so it
# tells a date line from a filename with no escaping question to answer.
#
# It has to be spelled two ways, and the reason is worth keeping: a literal NUL
# cannot be passed in an argument, because argv strings are NUL-terminated, so
# building the format with one raises ValueError before git is even reached.
# `%x00` is git's own escape and puts the byte in the *output*, where it is
# wanted, leaving the argument plain ASCII.
GIT_FORMAT = '%x00%cs'
NUL = '\x00'

GIT_TIMEOUT_SECONDS = 60


def _run_git(args, cwd):
    """Return git's stdout, or None if git is unavailable or unhappy.

    Every failure is the same answer to the caller, deliberately: this hook is a
    quality improvement to a sitemap, and no version of it is worth failing a
    documentation build over.

    The catch is broad on purpose, and on evidence rather than on principle: an
    earlier draft caught only OSError and SubprocessError, and the first thing
    that went wrong was neither. A narrow tuple that misses one class fails the
    build it promised not to.
    """
    try:
        result = subprocess.run(
            ['git', '-c', 'core.quotePath=false', *args],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
            check=True,
        )
    except Exception as exc:  # noqa: BLE001 - see the docstring
        log.warning('sitemap_lastmod: git unavailable (%s); keeping build dates.', exc)
        return None
    return result.stdout


def _repo_root(start):
    out = _run_git(['rev-parse', '--show-toplevel'], start)
    return Path(out.strip()) if out and out.strip() else None


def _last_commit_dates(root, docs_dir):
    """Map each tracked path under docs_dir to its most recent commit date.

    One `git log` walk for the whole tree rather than one call per page: 99
    subprocesses is real time on a build the deploy cron checks every five
    minutes.

    `%cs` is the committer date as a bare YYYY-MM-DD, which is the shape
    <lastmod> wants, so nothing here parses or reformats a timestamp. Merges are
    skipped because `--name-only` reports no paths for them anyway.
    """
    out = _run_git(
        ['log', '--no-merges', '--name-only', f'--pretty=format:{GIT_FORMAT}', '--', str(docs_dir)],
        root,
    )
    if out is None:
        return {}

    dates = {}
    commit_date = ''
    for line in out.splitlines():
        if line.startswith(NUL):
            commit_date = line[1:].strip()
        elif line and commit_date:
            # git log walks newest first, so the first date a path is seen with
            # is its latest. setdefault keeps that one and ignores the history.
            dates.setdefault(line, commit_date)
    return dates


def on_env(env, config, files, **kwargs):
    docs_dir = Path(config['docs_dir']).resolve()
    root = _repo_root(docs_dir)
    if root is None:
        return env

    dates = _last_commit_dates(root, docs_dir)
    if not dates:
        return env

    try:
        prefix = docs_dir.relative_to(root).as_posix()
    except ValueError:
        # docs_dir outside the repository: nothing in `dates` can key to it.
        return env

    dated = 0
    for file in files.documentation_pages():
        page = getattr(file, 'page', None)
        if page is None:
            continue
        key = file.src_uri if prefix == '.' else f'{prefix}/{file.src_uri}'
        commit_date = dates.get(key)
        if commit_date:
            page.update_date = commit_date
            dated += 1

    log.info('sitemap_lastmod: dated %d pages from git history.', dated)
    return env
