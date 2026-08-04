# Agent-Driven Screenshot Capture — Design

**Date:** 2026-08-04
**Status:** Approved design, awaiting implementation plan
**Repository:** this one (`adam-docs`). The application being captured lives in `~/dev/adam`.

**Driver:** `TODO.md` is mostly a queue of screenshots the manual needs and does not have. Each entry
already reads as an instruction to whoever takes the picture — which screen, which menu path, what to
frame, what the data must look like. Nothing in this repository lets an agent act on one. This design
adds that capability.

## What exists today

**The corpus.** 687 PNGs under `docs/assets/screenshots/<chapter-slug>/`, named
`<chapter-slug>-NN.png` with a two-digit zero-padded number. Widths cluster tightly in the 860–900
band (879, 864, 897, 880, 894, 875 …), consistent with a 900px viewport and a variable vertical crop.
Median file size 44 KB, mean 54 KB. All 666 Markdown references use an empty alt text and a path
relative to `docs/`, of the form `![](assets/screenshots/<chapter>/<file>.png)`.

**The framing style.** Captures are content-region crops in light mode: no browser chrome, no page
header or navigation, no arrows or highlight boxes. `two-factor-authentication-15.png` is
representative — it runs from a section heading down to a trailing action button, with roughly 8px of
margin, spanning several distinct elements rather than one.

**The application.** ADAM runs locally at `https://dev.theta.adam.co.za/`, served by local Apache2 install, backed by the `adam_dev` database, whose school is "Random College Demo". The certificate
is a valid Let's Encrypt wildcard, so no TLS workarounds are needed. Every asset on an ADAM page is
same-origin; the only external host in the markup is a `docs.google.com` feedback link, which is
never loaded.

**Login needs no credentials.** `config.dev.ini` sets `env = dev`, and
`ADAM\Security\DevLogin::attemptLogin` runs whenever the username or password is empty on a
non-production environment. `GET /login/staff` with both fields left blank and the **Login** button
clicked signs in as `staff_id` 1. The form carries a `_csrft` token, so the click must happen in a
real browser rather than as a bare POST.

**The bypass is more capable than it first appears**, and the design leans on this. `attemptLogin`
takes a login type and a username: a named `staff_username` signs in as that staff member, a parent
is found by ID number (falling back to the most recent family), and a pupil by username (falling back
to the most recent pupil). Briefs such as "**Families → Security → Login as a family** for a
demonstration family with more than one child" and the permission-scoped captures therefore need no
special provision — they are already possible.

## What this does not solve

`adam_dev` contains 2,536 pupils but neither **Brandon Dayne Jarred Clark** (48619) nor **Riley
Anderson** (99726), the example pupils `TODO.md` asks new captures to reuse so that each page reads as
one continuous example. New captures taken against this instance will introduce different names.

This is a known and accepted consequence of capturing against local dev. It is recorded here so that
it is a decision rather than a surprise: either the affected `TODO.md` entries get their example
pupils updated to names that exist in `adam_dev`, or a page accepts a discontinuity in its worked
example. It is not resolved by this design.

## A blocker in the environment, not in this design

**The staff dashboard is currently broken on the dev instance**, and the bypass login lands on it.
`GET /` after login returns 500:

```
ADAM\Security\UnknownPrivilegeException: Unknown privilege: assessment_results_edit
  Authorisation.php:198  ← Authorisation::staffPrivilegeIsOk (Authorisation.php:154)
  ← Reporting::mainPageWidget (Reporting.php:2137)
  ← DashboardController::showStaffDashboard (DashboardController.php:92)
```

The code asks for a privilege the `adam_dev` database does not know — consistent with the in-flight
work on permissions and the mark book editing window. It is pre-existing: `log_error` carries related
schema complaints daily since 2026-07-29, well before this design.

**It is only the dashboard.** The login itself succeeds and the session is sound —
`/menu/pupils`, `/menu/administration`, `/menu/reporting` and `/admin/language` all return 200 on the
same cookie. So the workflow navigates directly to the target screen after logging in rather than
dwelling on the dashboard, and everything except dashboard captures is unaffected.

Two consequences the plan carries: any brief that wants the dashboard itself is blocked until the
privilege is registered, and the first end-to-end task must target a non-dashboard screen.

## Architecture

Four new artefacts, plus two edits to files that already exist.

| File | Committed | Purpose |
|---|---|---|
| `.mcp.json` | no — gitignored | Local Playwright MCP configuration; holds the dev hostname |
| `.mcp.json.dist` | yes | Template carrying the shape without the hostname |
| `.claude/skills/capturing-screenshots/SKILL.md` | yes | The workflow and its conventions |
| `docs/assets/screenshots/<chapter>/captures.yml` | yes | Sidecar recording how each shot was taken |

This repository is public. `.mcp.json` stays out of git because it names an internal host resolving to
a private address; `.mcp.json.dist` carries everything else, with the hostname reduced to a
`https://dev.example.adam.co.za/` placeholder, so a second machine is one `cp` and one edit away. The
split follows the precedent ADAM itself sets with `config.ini` and `config.ini.dist`.

The two edits to existing files:

- **`.gitignore`** gains `.mcp.json`, in the same manner as the entries already there for `site/` and
  `.venv/`.
- **`README.md`** currently promises that "the capture workflow is documented in `scripts/README.md`
  (forthcoming)". That file does not exist. The promise is redirected to the skill.

### The MCP server

`@playwright/mcp`, pinned at `0.0.78`. Flags:

- `--browser chromium` **and** `--executable-path
  /home/philip/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`. Both are required. Left to
  itself the server tries the `chrome` channel at `/opt/google/chrome/chrome`, which is not installed;
  asking for `chromium` alone makes it demand a separate `chrome-for-testing` download. Pointing it at
  the already-cached `chromium-1217` binary avoids downloading a browser at all.
- `--viewport-size 900x1200` — the 900px width the corpus is built on, tall enough that most panels
  fit without scrolling.
- `--allowed-origins https://dev.theta.adam.co.za` — the safety rail. The browser cannot load a
  school's production ADAM. Because ADAM's pages are entirely same-origin, this costs nothing in
  rendering fidelity.
- `--isolated` — browser profile held in memory, never written to disk.
- `--headless` — droppable when someone wants to watch a run.
- `--output-dir` for the server's own console logs and page snapshots.

The origin allowlist is the mechanism that enforces `CONTRIBUTING.md`'s standing rule that screenshots
are never captured against a live site. It is a configuration boundary rather than an instruction an
agent has to remember. Verified: a navigation to `https://example.com/` fails with
`net::ERR_BLOCKED_BY_CLIENT`.

**Where images land.** `browser_take_screenshot`'s `filename` is *not* resolved against `--output-dir`;
it becomes `page.screenshot({path: <filename>})`, relative to the server process's working directory.
Since Claude Code launches the server from the repository root, a `filename` of
`docs/assets/screenshots/<chapter>/<name>.png` writes the image straight to its final home. The skill
uses that directly rather than capturing to scratch and copying.

## Capture conventions

**Viewport** fixed at 900×1200, captured with `scale: "css"` so a 900px viewport yields a 900px image
rather than a 1800px retina one.

**Two framing modes.** `browser_take_screenshot` accepts either an element target or `fullPage`; it has
**no `clip` parameter**, so an arbitrary rectangle cannot be requested directly. The modes are shaped
around that limit:

1. **Element** — one CSS selector passed as `target`; screenshot that element. Covers most panels,
   tables and fieldsets. Verified: `#body` on the administration menu yields an 844px-wide image,
   squarely inside the corpus's 860–900 band.

2. **Vertical span** — for the "a row plus the rows above and below" briefs the manual is full of.
   `browser_evaluate` computes the union bounding box of the wanted elements; `browser_resize` sets the
   viewport to 900 × (span height + 2 × padding); a `window.scrollTo` puts the span's top edge at the
   viewport top; then a plain viewport screenshot is taken. Verified end to end: a 2254px span produced
   a 900×2270 image, exactly the requested height.

   This is the same operation as the manual practice it replaces — resize the view, then crop
   vertically — and it needs no image library, which matters because Pillow is not installed and no PNG
   tooling exists on this machine.

Padding defaults to 8px, matching the margin visible in existing captures.

**Light mode always.** The theme toggle sits in the page footer and persists across pages, so it is
verified before capturing rather than assumed. Verified: `document.body` computes to
`rgb(239, 246, 255)` on a fresh isolated profile, so light is the starting state.

**Keep clear of the development banner.** Every page on the dev instance opens with a blue
**"Development Environment: Not for General Use"** banner, above the school name and menu. It must
never appear in a capture. In practice the content crops start well below it, but a careless
`fullPage` or a span that reaches the top of the document would include it.

**No annotations.** The corpus contains no arrows, callouts or highlight boxes. Adding them now would
make new images read as foreign.

**Naming.** `docs/assets/screenshots/<chapter-slug>/<chapter-slug>-NN.png`, two digits, zero-padded. A
re-capture keeps its existing number and filename — several `TODO.md` entries depend on this, because
the Markdown reference is already in place and must not need editing.

**Markdown references** match the house style exactly: empty alt text, path relative to `docs/`.

**Setting the shot up.** Several briefs require changing the demonstration school before the picture
means anything — granting **View birthdays**, giving **Markbook Entry** a window that has already
closed, moving a pupil's date of birth to today. This is done through ADAM's own interface as a super
user, never by writing to `adam_dev` directly, so the capture exercises the same path a school would.
Where a brief says to put something back, the sidecar records what changed so the revert is verifiable
rather than remembered.

### The sidecar

One `captures.yml` per chapter folder, beside the images:

```yaml
- image: parent-and-pupil-portal-09.png
  captured: 2026-08-04
  as: staff            # or: parent / pupil, with the identity used
  path: Pupils tab → Security → Manage permissions groups → privileges
  frame:
    mode: span
    from: "#privileges h3:has-text('Birthdays')"
    to: "tr:has(td:text('View birthdays'))"
  setup: "Ticked View birthdays for both Pupils and Families on the demo families' group"
  revert: none
```

Enough to re-shoot the same crop a year later; cheap enough that it does not become a chore. It grows
only as images are captured. The existing 687 are not back-filled.

This exists because re-capture is the dominant maintenance task. `TODO.md` asks for "re-capture the
same crop, keeping the filename" twice on a single page, and each time the person doing it has to
rediscover the framing from scratch.

## The workflow

The skill drives a checklist, one todo per step:

1. **Take the brief** — from a `TODO.md` entry or from the user. Restate what the image must show
   before opening a browser.
2. **Start the browser** and confirm the origin lock is live: a navigation to any host other than the
   dev instance must fail.
3. **Log in** as the role the brief needs — staff by default, or a named staff member, parent or pupil
   where the shot demands it.
4. **Set the demonstration school up** if the brief calls for it, through the interface, recording what
   changed.
5. **Navigate** to the screen, following the menu path in the brief.
6. **Confirm light mode**, then frame and capture.
7. **Look at the result.** Read the saved PNG back and check it against the brief: is every named
   element in shot, is anything cut off, is there real-looking data that should not be there.
8. **Place it** — write the `![](assets/screenshots/…)` reference at the point the brief describes.
9. **Record it** in `captures.yml`, and revert any setup the brief says to revert.
10. **Strike the entry** from `TODO.md`, per that file's own standing rule, and commit.

Step 7 carries the most weight. The agent can see what it captured, so a wrong crop caught there costs
nothing, whereas a wrong crop that ships is a page that misleads a reader.

## Failure handling

Every one of these ends in a report, never in a substitute image.

- **Element not found, or the page looks unfamiliar.** Stop. Do not capture something adjacent and
  hope. Report which selector failed and what the page actually showed.
- **The feature is not on this build.** Anticipated already: the Pupil Overview permission wording is
  "one build out of date". Report that the instance cannot yet produce the shot and leave the `TODO.md`
  entry standing.
- **The demonstration data will not cooperate.** The 2FA dashboard card "could not be made to appear on
  the demonstration server", and the manual went without a picture. That is a legitimate outcome.
- **The brief carries an open question.** The heads-of-subject entry ends with a discrepancy to raise
  with development. Surface it; do not paper over it in the manual.
- **The dev instance is unreachable.** Check before starting and fail fast, rather than part-way
  through a run.

## Deliberately out of scope

**PNG optimisation.** No optimiser is installed, and Playwright's output for a 900px-wide light
interface lands in the same 40–60 KB band as the existing median. A compression step would be
machinery with nothing to do.

**A capture manifest and runner.** A checked-in recipe per image with an `npm run capture` command was
considered and rejected as over-building. The `captures.yml` sidecar records the same information at a
fraction of the cost and rots gracefully if it falls out of use.

**Alt text.** All 666 image references have empty alt text, so the manual's screenshots are invisible
to screen readers. The skill matches the house convention rather than diverging mid-corpus. Fixing
this is worth its own piece of work and is not attempted here.

**Back-filling sidecars** for the existing 687 images.
