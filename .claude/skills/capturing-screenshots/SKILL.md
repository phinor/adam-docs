---
name: capturing-screenshots
description: Use when capturing or re-capturing a screenshot for the ADAM manual — taking a brief from TODO.md or the user, driving the dev instance in a browser, framing the shot to house conventions, and placing it in the manual with its provenance recorded
---

# Capturing Screenshots for the ADAM Manual

Screenshots are captured against the local ADAM dev instance at
`https://dev.theta.adam.co.za/`, never against a school's live site. The Playwright MCP server is
configured so the browser physically cannot reach anything else.

## Before you start

Confirm the instance is up:

```bash
curl -sk -o /dev/null -w "%{http_code}\n" --max-time 10 https://dev.theta.adam.co.za/login/staff
```

Expected `200`. Anything else — stop and report; do not begin a capture run.

## Logging in

No credentials exist or are needed. `env = dev` enables a bypass:

1. `browser_navigate` to `https://dev.theta.adam.co.za/login/staff`
2. `browser_click` the **Login** button, `target: "#login-button"`, leaving both fields empty

This signs you in as `staff_id` 1.

The login lands on the staff dashboard. If it returns a 500 rather than the dashboard, the session is
still sound — navigate straight to the screen you need, and only stop if the brief wants the dashboard
itself.

To be somebody else, go to the login page for that role, fill in the **Login Name** field only, leave
**Password** empty, and click **Login**:

- **A named staff member** — `/login/staff`, their `staff_username`.
- **A parent** — `/login/parent`, a family member's ID number. Left blank, you get the most recently
  created family.
- **A pupil** — `/login/pupil`, their username. Left blank, you get the most recently created pupil.

Use this for briefs that need a particular permission set, or a parent's view of the portal.

## Framing

The viewport is fixed at 900×1200 and screenshots are taken with `scale: "css"`, so a 900px viewport
yields a 900px image. Padding defaults to 8px.

**Mode 1 — element.** One CSS selector, passed as `target` to `browser_take_screenshot`. Use this
whenever the region is a single panel, table or fieldset.

**Mode 2 — vertical span.** For "this row plus the rows above and below". There is no `clip`
parameter, so measure, resize, scroll, then shoot:

1. `browser_evaluate` to measure the union box:

```js
() => {
  const els = Array.from(document.querySelectorAll('<your selectors>'));
  if (!els.length) return {error: 'no match'};
  const rs = els.map(e => e.getBoundingClientRect());
  const top = Math.min(...rs.map(r => r.top)) + scrollY;
  const bot = Math.max(...rs.map(r => r.bottom)) + scrollY;
  return {top: Math.round(top), height: Math.round(bot - top)};
}
```

2. `browser_resize` to `width: 900`, `height: height + 16`
3. `browser_evaluate` — `() => { window.scrollTo(0, <top - 8>); return Math.round(scrollY); }`
4. `browser_take_screenshot` with no `target`, capturing the viewport

Check the returned `scrollY` matches what you asked for. If the page is too short to scroll that far,
the crop will be wrong — resize taller, or frame from an element instead.

## House rules

- **Light mode always.** Verify before capturing:
  `() => getComputedStyle(document.body).backgroundColor` must be `rgb(239, 246, 255)`. The footer
  toggle persists across pages.
- **Never include the development banner** — the blue "Development Environment: Not for General Use"
  strip at the top of every page.
- **No browser chrome, no page header or navigation**, unless the brief explicitly asks for it.
- **No annotations.** The manual has no arrows or highlight boxes anywhere; adding them would make
  new images look foreign.
- **No real school data.** The dev instance holds a randomised demonstration school, which is why it
  is the only host the browser can reach.

## Naming and placement

`browser_take_screenshot`'s `filename` resolves against the repository root, not `--output-dir`, so
write straight to the destination:

```
docs/assets/screenshots/<chapter-slug>/<chapter-slug>-NN.png
```

Two digits, zero-padded. A re-capture **keeps its existing filename** — the Markdown reference is
already in place and must not need editing.

Reference it with empty alt text and a path relative to `docs/`:

```markdown
![](assets/screenshots/<chapter-slug>/<chapter-slug>-NN.png)
```

## Setting a shot up

Many briefs need the school configured before the picture means anything — a permission granted, a
date moved, a time frame closed. Do it **through ADAM's interface**, never by writing to `adam_dev`
directly, so the capture exercises the path a school would take. Record what you changed, and put it
back if the brief says to.

## Recording what you did

Append to `docs/assets/screenshots/<chapter-slug>/captures.yml`, creating it if absent:

```yaml
- image: parent-and-pupil-portal-09.png
  captured: 2026-08-04
  as: staff
  path: Pupils tab → Security → Manage permissions groups → privileges
  frame:
    mode: span
    selectors: "#privileges tr:has(td:text('View birthdays'))"
    padding: 8
  setup: "Ticked View birthdays for both Pupils and Families on the demo families' group"
  revert: none
```

Existing images are not back-filled; the file grows only as shots are taken.

## The checklist

1. Restate what the image must show, before opening a browser.
2. Confirm the instance is up.
3. Log in as the role the brief needs.
4. Set the school up, if the brief calls for it.
5. Navigate to the screen.
6. Confirm light mode.
7. Frame and capture.
8. **Read the saved PNG back and check it against the brief** — every named element in shot, nothing
   cut off, no development banner, no data that should not be there.
9. Write the Markdown reference where the brief says.
10. Append to `captures.yml`; revert any setup that should be reverted.
11. Remove the entry from `TODO.md` — that file's own standing rule.
12. Run `docker run --rm --user "$(id -u):$(id -g)" -v "$(pwd):/docs" -w /docs squidfunk/mkdocs-material:latest build --strict --site-dir /docs/.build-verify` and confirm it exits 0, then `rm -rf .build-verify`.
13. Commit.

Step 8 is the one that matters. You can see what you captured — a wrong crop caught there costs
nothing, while a wrong crop that ships is a page that misleads a reader.

## When it goes wrong

Every one of these ends in a report, never a substitute image.

- **Selector matches nothing, or the page looks unfamiliar.** Stop. Do not capture something adjacent
  and hope. Report which selector failed and what was actually on the page.
- **The feature is not on this build.** Report it and leave the `TODO.md` entry standing.
- **The data will not cooperate.** A section reading well without a picture is a legitimate outcome —
  the 2FA dashboard card was left without one for exactly this reason.
- **The brief carries an open question.** Surface it. Do not paper over a discrepancy in the manual.
- **The dev instance is unreachable.** Fail fast and say so.
