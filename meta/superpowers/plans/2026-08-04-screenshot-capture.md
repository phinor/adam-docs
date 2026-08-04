# Agent-Driven Screenshot Capture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let an agent take a screenshot brief from `TODO.md` and produce the finished image, its Markdown reference and its provenance record, without a human touching a browser.

**Architecture:** A Playwright MCP server, locked by configuration to the local ADAM dev instance, gives the agent eyes and hands in the browser. A project skill carries the workflow and the framing conventions. A per-chapter `captures.yml` records how each shot was taken so it can be re-shot identically.

**Tech Stack:** `@playwright/mcp` 0.0.78, cached Chromium 1217, MkDocs Material (built via Docker), ADAM on PHP at `https://dev.theta.adam.co.za/`.

**Design:** `meta/superpowers/specs/2026-08-04-screenshot-capture-design.md`

## Global Constraints

- Viewport is **900×1200**; screenshots are taken with `scale: "css"` so a 900px viewport yields a 900px image.
- Padding around a framed region defaults to **8px**.
- **Light mode always.** `document.body` must compute to `rgb(239, 246, 255)` before capturing.
- The blue **"Development Environment: Not for General Use"** banner must never appear in a capture.
- Images are named `docs/assets/screenshots/<chapter-slug>/<chapter-slug>-NN.png`, two digits, zero-padded. A re-capture keeps its existing filename.
- Markdown references use empty alt text and a path relative to `docs/`: `![](assets/screenshots/<chapter>/<file>.png)`.
- No annotations — no arrows, callouts or highlight boxes.
- The browser may only reach `https://dev.theta.adam.co.za`. Never a school's production ADAM.
- Prose follows `CONTRIBUTING.md`: British/South African spelling, UI labels in bold.
- The staff dashboard returned 500 (`UnknownPrivilegeException: assessment_results_edit`) while this plan was being written. It was fixed on 2026-08-04 and now renders normally, so dashboard captures are not blocked.

---

### Task 1: MCP server configuration and the origin rail

**Files:**
- Create: `/home/philip/dev/adam-docs/.mcp.json.dist`
- Create: `/home/philip/dev/adam-docs/.mcp.json`
- Modify: `/home/philip/dev/adam-docs/.gitignore`

**Interfaces:**
- Produces: an MCP server named `playwright` exposing `browser_navigate`, `browser_click`, `browser_evaluate`, `browser_resize`, `browser_take_screenshot`, `browser_snapshot`, `browser_find`, `browser_fill_form`, `browser_select_option`, `browser_wait_for`. Tasks 2 and 3 depend on these tool names.

- [ ] **Step 1: Write the committed template**

Create `.mcp.json.dist`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y", "@playwright/mcp@0.0.78",
        "--headless",
        "--isolated",
        "--browser", "chromium",
        "--executable-path", "/home/philip/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome",
        "--viewport-size", "900x1200",
        "--allowed-origins", "https://dev.example.adam.co.za",
        "--output-dir", "/tmp/adam-docs-capture"
      ]
    }
  }
}
```

Both `--browser` and `--executable-path` are required. Without them the server looks for the `chrome` channel at `/opt/google/chrome/chrome`, which is not installed; with `--browser chromium` alone it demands a separate `chrome-for-testing` download.

- [ ] **Step 2: Create the local copy with the real host**

```bash
cd /home/philip/dev/adam-docs
sed 's#https://dev.example.adam.co.za#https://dev.theta.adam.co.za#' .mcp.json.dist > .mcp.json
grep allowed-origins -A1 .mcp.json
```

Expected: the line after `--allowed-origins` reads `"https://dev.theta.adam.co.za"`.

- [ ] **Step 3: Keep the local copy out of git**

Append to `.gitignore`, after the `# Python bytecode` block:

```
# Local Playwright MCP config (names the internal dev host; see .mcp.json.dist)
.mcp.json
```

- [ ] **Step 4: Verify git ignores it**

Run: `cd /home/philip/dev/adam-docs && git status --porcelain`
Expected: `.mcp.json.dist` appears as untracked (`??`); `.mcp.json` does **not** appear at all.

- [ ] **Step 5: Load the server**

The MCP server is read at startup, so Claude Code must be restarted before its tools exist. Restart, then confirm the `playwright` server is connected via `/mcp`.

- [ ] **Step 6: Verify the origin rail blocks the outside world**

Call `browser_navigate` with `url: "https://example.com/"`.
Expected: **an error** containing `net::ERR_BLOCKED_BY_CLIENT`. If this navigation succeeds, stop — the safety rail is not working and no capture may proceed.

- [ ] **Step 7: Verify the dev instance loads**

Call `browser_navigate` with `url: "https://dev.theta.adam.co.za/login/staff"`, then `browser_evaluate` with:

```js
() => ({ title: document.title, bg: getComputedStyle(document.body).backgroundColor })
```

Expected: `title` is `Random College Demo's ADAM` and `bg` is `rgb(239, 246, 255)`.

Note: a `browser_navigate` immediately after a blocked navigation can report a spurious "interrupted by another navigation" error. Repeat the call once before treating it as a real failure.

- [ ] **Step 8: Commit**

```bash
cd /home/philip/dev/adam-docs
git add .mcp.json.dist .gitignore
git commit -m "NEW: Playwright MCP configuration for screenshot capture

Locks the browser to the local dev instance by configuration, so a capture run
cannot reach a school's production ADAM. The local .mcp.json is ignored because
it names the internal host; .mcp.json.dist carries the shape, following the
config.ini/config.ini.dist convention ADAM itself uses.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: The capture skill

**Files:**
- Create: `/home/philip/dev/adam-docs/.claude/skills/capturing-screenshots/SKILL.md`
- Modify: `/home/philip/dev/adam-docs/README.md` (the `## Screenshots` section)

**Interfaces:**
- Consumes: the `playwright` MCP tools from Task 1.
- Produces: a skill invocable as `capturing-screenshots`, and the `captures.yml` schema that Task 3 writes.

- [ ] **Step 1: Write the skill**

The full text of `.claude/skills/capturing-screenshots/SKILL.md` was drafted here as this plan was
being written. It has since drifted from what shipped, so it is not reproduced in this plan any more —
the shipped file is authoritative and this one is not kept in sync with it. In particular, the
version drafted here still treated the staff dashboard as broken and told the reader to stop and
report it as blocked, which is no longer true (see the Global Constraints note above); it also lacked
the font pre-flight section and its checklist ran to 13 steps rather than the shipped 14. Read
`.claude/skills/capturing-screenshots/SKILL.md` directly for the current text — git history holds the
original draft if it is ever needed.

- [ ] **Step 2: Redirect the README's dangling promise**

`README.md` currently says the capture workflow is documented in `scripts/README.md`, which does not exist. Replace the `## Screenshots` section body with:

```markdown
Screenshots are captured against the local ADAM dev instance, never against production. An agent can
capture them: see the `capturing-screenshots` skill in
[`.claude/skills/capturing-screenshots/SKILL.md`](.claude/skills/capturing-screenshots/SKILL.md), and
copy `.mcp.json.dist` to `.mcp.json` with the dev host filled in.
```

- [ ] **Step 3: Verify the skill is discoverable**

Restart Claude Code, then confirm `capturing-screenshots` appears in the available skills list.
Expected: present, with the description from the frontmatter.

- [ ] **Step 4: Verify the build still passes**

```bash
cd /home/philip/dev/adam-docs
docker run --rm --user "$(id -u):$(id -g)" -v "$(pwd):/docs" -w /docs \
    squidfunk/mkdocs-material:latest build --strict --site-dir /docs/.build-verify
echo "EXIT=$?"
rm -rf .build-verify
```

Expected: `EXIT=0`.

- [ ] **Step 5: Commit**

```bash
cd /home/philip/dev/adam-docs
git add .claude/skills/capturing-screenshots/SKILL.md README.md
git commit -m "NEW: Skill for capturing manual screenshots

Carries the capture workflow: the dev bypass login, the 900px viewport, the two
framing modes, and the rule that a capture is read back and checked before it
ships. Also redirects the README's promise of a scripts/README.md that was never
written.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Capture `parent-and-pupil-portal-09.png` end to end

The first real brief, chosen because it needs no dashboard and its setup *is* the picture.

From `TODO.md`, *Parent and Pupil Portal — Today's Birthdays*, item 1:

> **Pupils → Security → Manage permissions groups**, then **privileges** against the group the
> demonstration families belong to. Scroll to the **Birthdays** heading. Frame the **View birthdays**
> row with both its **Pupils** and **Families** tick boxes visible, and enough of the rows above and
> below to show it sitting in the same list as everything else. Both boxes ticked.

**Files:**
- Create: `/home/philip/dev/adam-docs/docs/assets/screenshots/parent-and-pupil-portal/parent-and-pupil-portal-09.png`
- Create: `/home/philip/dev/adam-docs/docs/assets/screenshots/parent-and-pupil-portal/captures.yml`
- Modify: `/home/philip/dev/adam-docs/docs/parent-and-pupil-portal.md:153` (insert after)
- Modify: `/home/philip/dev/adam-docs/TODO.md` (remove the completed entry)

**Interfaces:**
- Consumes: the `playwright` MCP tools (Task 1) and the `capturing-screenshots` skill (Task 2).

- [ ] **Step 1: Invoke the skill**

Invoke `capturing-screenshots` and follow its checklist. The steps below are the specifics for this brief.

- [ ] **Step 2: Log in and reach the permissions screen**

`browser_navigate` to `https://dev.theta.adam.co.za/login/staff`, `browser_click` `#login-button`, then navigate to the **Pupils** menu and follow **Security → Manage permissions groups**. Use `browser_snapshot` to find the links rather than guessing URLs.

- [ ] **Step 3: Find the group the demonstration families use**

Open **privileges** against the pupil login group the demonstration families belong to. If more than one group could qualify, pick the one with families assigned and note which in the sidecar.

- [ ] **Step 4: Tick both boxes under Birthdays**

Scroll to the **Birthdays** heading and tick **View birthdays** for both **Pupils** and **Families**, then save.

If there is no **Birthdays** heading or no **View birthdays** permission, **stop**: the feature is not on this build. Report it and leave the `TODO.md` entry standing.

- [ ] **Step 5: Verify light mode**

`browser_evaluate`: `() => getComputedStyle(document.body).backgroundColor`
Expected: `rgb(239, 246, 255)`.

- [ ] **Step 6: Frame the span and capture**

Measure the **View birthdays** row plus roughly two rows either side, then resize, scroll and shoot per the skill's mode 2. Write to `docs/assets/screenshots/parent-and-pupil-portal/parent-and-pupil-portal-09.png`.

- [ ] **Step 7: Check the image dimensions**

```bash
cd /home/philip/dev/adam-docs
python3 -c "
import struct
f='docs/assets/screenshots/parent-and-pupil-portal/parent-and-pupil-portal-09.png'
d=open(f,'rb').read(33); w,h=struct.unpack('>II',d[16:24]); print(w,'x',h)"
```

Expected: width `900`, or between 860 and 900 if framed as an element. A width outside that band means the viewport was wrong.

- [ ] **Step 8: Read the image back and check it**

Read the PNG. Confirm: the **View birthdays** row is present with both tick boxes ticked and visible; rows above and below are in shot; no development banner; nothing cut off mid-row.

If any of these fail, re-frame and re-capture before going on.

- [ ] **Step 9: Place the reference**

In `docs/parent-and-pupil-portal.md`, insert after line 153 (the paragraph ending "both as viewers and as names in the list."), separated by a blank line:

```markdown
![](assets/screenshots/parent-and-pupil-portal/parent-and-pupil-portal-09.png)
```

- [ ] **Step 10: Write the sidecar**

Create `docs/assets/screenshots/parent-and-pupil-portal/captures.yml` with one entry, following the schema in the skill. Record the actual group name used, the actual selectors, and `revert: none` — the permission is meant to stay granted for images 2 and 3 of the same brief.

- [ ] **Step 11: Strike the completed entry from TODO.md**

Remove only item 1 (`parent-and-pupil-portal-09.png`) from the *Parent and Pupil Portal — Today's Birthdays* section. Items 2 and 3 stay, and so does the paragraph about granting **View birthdays** and setting **Birthdays visible in the portal**, because they still apply to those two.

- [ ] **Step 12: Verify the build**

```bash
cd /home/philip/dev/adam-docs
docker run --rm --user "$(id -u):$(id -g)" -v "$(pwd):/docs" -w /docs \
    squidfunk/mkdocs-material:latest build --strict --site-dir /docs/.build-verify
echo "EXIT=$?"
rm -rf .build-verify
```

Expected: `EXIT=0`. A missing image aborts the build with "contains a link ... but the target is not found", so this genuinely checks the reference resolves.

- [ ] **Step 13: Commit**

```bash
cd /home/philip/dev/adam-docs
git add docs/assets/screenshots/parent-and-pupil-portal/ docs/parent-and-pupil-portal.md TODO.md
git commit -m "NEW: Capture the View birthdays permission for the portal page

The first screenshot taken by an agent against the dev instance, and the first
entry in a captures.yml recording how a shot was framed.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

## Notes for whoever runs this

**Restarts.** Tasks 1 and 2 both need Claude Code restarted before their output is live — the MCP server and the skill are read at startup.

**`site.old/`** in the repository root is untracked debris from a build that predates the `--user` flag in `bin/build.sh`. Its contents are root-owned, so `bin/build.sh --dev` fails at its cleanup step with "Permission denied". It needs `sudo rm -rf site.old`, which is outside this plan.

**Example pupils.** `adam_dev` has neither Brandon Clark (48619) nor Riley Anderson (99726), the pupils `TODO.md` asks captures to reuse. Captures from this instance will show different names. This is unresolved by design — see the spec.
