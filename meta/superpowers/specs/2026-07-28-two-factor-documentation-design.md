# Two-Factor Authentication Documentation — Design

**Date:** 2026-07-28
**Status:** Approved design, awaiting implementation plan
**Programme:** Phase 2, Workstream B of the ADAM security hardening master plan
(`~/dev/adam/docs/superpowers/plans/2026-07-27-security-hardening-master-plan.md`) — the last
workstream in Phase 2.
**Repository:** this one (`adam-docs`). The code changes it documents live in `~/dev/adam` and have
shipped in PRs #397, #398, #399, #403 and #405.

**Driver:** two-factor authentication becomes mandatory for all staff on **1 January 2027**, and four
workstreams of code have shipped that the published manual does not describe. Some of what it does
say is now wrong.

## What is wrong today

**`docs/logging-on-to-adam.md` states the opposite of how ADAM now behaves**, in the strongest form,
twice:

- Line 22: "A successful passkey login satisfies the Two-Factor Authentication requirement on its
  own."
- Lines 67-71: "This is true even when the **Two Factor Authentication Forced for Staff** setting
  … is enabled. … The Two-Factor Authentication setting therefore continues to govern password-based
  logins, and is **unaffected by passkey enrolment**."

A passkey waives the login-time *prompt*. It does not waive the *requirement to enrol*, because the
account's password remains a live credential — anyone who obtains it must still be stopped by the
second factor. An administrator reading that page today would conclude their passkey users are
exempt from a policy they are not exempt from.

**`docs/two-factor-authentication.md` frames enrolment as optional throughout** — "Compulsory
Enrolment" and "Voluntary Enrolment" as parallel equal paths, a school-level switch, and advice to
build adoption "before it becomes a mandatory requirement". That framing does not survive the
mandate.

**The lost-phone advice is wrong in a way that matters most when it is read.** Three FAQ answers say
some version of "the short answer is that you can't", routing every case to an administrator.
Recovery codes now exist and are not mentioned anywhere in the manual.

**Four features are undocumented entirely:** recovery codes, the remembered-devices card and
sign-out, the administrator coverage screen, and the dashboard prompt widget.

## Structure

Split by audience, following the existing `security-administration-for-staff.md` /
`security-administration-for-families-and-pupils.md` precedent.

### `docs/two-factor-authentication.md` — the staff guide

Rewritten rather than patched. It opens with what a staff member needs: that two-factor
authentication is required for all staff from 1 January 2027, and how to set it up.

- **The mandate**, stated plainly and dated, replacing the voluntary/compulsory dual framing.
- **Enrolment**, restructured to the two-step, two-card page that shipped — a numbered step for
  scanning and a numbered step for confirming, with the authenticator-app recommendations presented
  as the aside they now are rather than as a preamble.
- **Recovery codes** — ten, single-use, shown once at enrolment, printable and downloadable, and
  regenerable from the management page. New material.
- **Remembered devices** — what "remember this computer" means from the staff member's side, the
  count they see, and signing every device out. New material.
- **Losing your phone**, rewritten: use a recovery code; ask an administrator only if you have none
  left. The existing three FAQ answers collapse into this.
- **Passkeys**, corrected: signing in with a passkey means no code prompt, but enrolment is still
  required.

### `docs/two-factor-authentication-for-administrators.md` — new

- **The mandate and what to do before it** — the phased-adoption advice, rewritten around a deadline
  rather than a decision.
- **The settings**: *Two Factor Authentication Forced For Staff*, the OTP frequency method, and
  *Remember logged-in machines for*. Moved here from the staff page and from
  `logging-on-to-adam.md`, which currently duplicates them.
- **The coverage screen** — the four segments, the "N of M staff are set up" headline, what each
  segment means, and why a staff member who is suspended but enrolled appears under **Set up**
  rather than **Suspended**.
- **The dashboard prompt** and how its tone escalates as the date approaches.
- **Per-staff actions** — removing someone's second factor, which requires re-authentication, and
  signing their remembered devices out, which notifies them.

### Corrections elsewhere

- **`docs/logging-on-to-adam.md`** — both passkey passages corrected; the duplicated settings
  descriptions replaced by links to the administrator page.
- **`docs/passkey-authentication.md`** — the prompt-versus-enrolment distinction added to the
  "How is a passkey different from Two-Factor Authentication?" answer.
- **`mkdocs.yml`** — the new page added to `nav`, alphabetically, as the list requires.

## Conventions

From `CONTRIBUTING.md`, and matching the surrounding pages:

- British/South African spelling — **enrolment**, not enrollment.
- UI labels in bold: "click on the **Save** button".
- **Menu paths as sentences, not arrows.** `two-factor-authentication.md` currently violates this
  ("**Staff → Security Administration → Manage Two-Factor Authentication**"). Since the page is being
  rewritten, the violation is fixed rather than carried over.
- Admonitions limited to the four in use across the site: `note`, `tip`, `warning`, `danger`.
- Images under `docs/assets/screenshots/<page-slug>/`, named `<page-slug>-NN.png`.

**One deliberate departure.** Existing images on the 2FA page use empty alt text (`![](…)`) with the
description as a following paragraph. New images get real alt text. The existing convention is
invisible to anyone using a screen reader, it costs nothing to improve, and the following-paragraph
captions stay where they are useful sighted context.

## Accuracy

Every factual claim is checked against the shipped code as it is written — the number of recovery
codes, what each segment means, what each setting does, what an administrator's action notifies.

This is not pedantry about process. This programme has fixed six separate defects where a message
asserted something the code could not know, and a manual that describes intended rather than actual
behaviour is the same defect in a different medium — with a longer half-life, because nobody
re-reads it against the code.

## Screenshots

Text is written now; captures follow. Every image needed is added to `TODO.md` in that file's
established format — the page it belongs to, how to reach the screen, what to frame, and what the
data should look like — against the demonstration school, never a live site.

Needed:

- Replacements for `two-factor-authentication-04` through `-07`, which show the old single-page
  enrolment flow.
- The recovery-code screen as shown once at enrolment.
- The remembered-devices card.
- The coverage screen with its headline and segments.
- The dashboard prompt widget.

`-08` and `-09` (the removal flow) are checked against the rebuilt page and listed only if they no
longer match.

## Out of scope

- **`docs/logging-on-to-adam-a-guide-for-parents.md`.** The mandate is staff-only, and the parents'
  guide carries no two-factor content today. That stays true.
- **Taking the screenshots.** They need a demonstration tenant and a browser.
- **The announcement to schools.** A separate deliverable of the master plan, drafted and unsent.
- **Families and pupils.** Phase 5 of the programme.

## Success criteria

- No page claims a passkey login exempts anyone from enrolling.
- A staff member who has lost their phone finds the recovery-code answer before the "contact your
  administrator" answer.
- An administrator can find out what the coverage screen's four segments mean without opening it.
- Every new claim in the manual matches what the code does.

## Rejected alternatives

- **Keeping one page.** Matches `passkey-authentication.md`'s "For Administrators" closing section,
  but the page roughly doubles and the staff member's own instructions end up further from the top.
- **Splitting recovery codes onto their own page.** They are what a locked-out user needs fastest,
  which argues for findability — but a page they reach only when already locked out is worse than a
  section on the page they were told to read when they enrolled.
- **Holding the sweep until screenshots exist.** Nothing published gets less wrong in the meantime.
- **Documenting current behaviour and holding the mandate date** until the announcement is sent.
  Rejected deliberately: schools reading ahead should be able to find the deadline.
