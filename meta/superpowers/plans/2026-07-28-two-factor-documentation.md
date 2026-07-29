# Two-Factor Authentication Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring the published ADAM manual in line with two-factor authentication as it now works — mandatory for all staff from 1 January 2027, with recovery codes, remembered-device sign-out, and an administrator coverage screen — and remove the passages that state the opposite.

**Architecture:** `docs/two-factor-authentication.md` is rewritten as the staff guide. A new `docs/two-factor-authentication-for-administrators.md` takes the settings and every administrator-facing surface. Two other pages lose passages that are now wrong. Screenshots are not taken; each one needed is written into `TODO.md`.

**Tech Stack:** MkDocs with a custom theme; `docs/*.md` are the sources and `site/` is generated output that is **never hand-edited**.

## Global Constraints

Every one of these comes from `CONTRIBUTING.md` or from the surrounding pages. They bind every task.

- **British/South African spelling.** "enrolment", not "enrollment". "organise", "colour".
- **UI labels in bold**: "click on the **Save** button".
- **Menu paths as sentences, never arrows.** Write "click on the **Staff tab**, then under the **Security Administration** heading, click on **Manage your Two-Factor Authentication**". Do **not** write "Staff → Security Administration → …". The existing 2FA page violates this; the violation is fixed, not carried over.
- **The two menu entries, verbatim from `includes/menu/menu.php`:**
  - Staff tab, Security Administration: **Manage your Two-Factor Authentication**
  - Administration tab, Security Administration: **Manage Two-Factor Authentication for staff**
  The current manual says "Manage Two-Factor Authentication" and "Manage Two Factor Administration". Both are wrong; correct them wherever they appear.
- **Headings:** one `#` for the page title, `##` for a section, `###` for a sub-section. FAQ entries are `###` written as full questions.
- **Admonitions:** only `!!! note`, `!!! tip`, `!!! warning`, `!!! danger`. Body indented four spaces.
- **Images** live at `docs/assets/screenshots/<page-slug>/<page-slug>-NN.png`, two-digit sequence.
- **New images get real alt text** — `![The recovery codes screen](…)`. This departs from the page's existing empty-alt convention deliberately; do not change existing image tags you are not otherwise touching.
- **No screenshots are taken in this plan.** Where one is needed, write the `TODO.md` entry instead.
- **Never invent behaviour.** Every factual claim must match the shipped code. Where this plan gives you a fact, it has been checked. If you find yourself unsure of one, say so in your report rather than writing a plausible sentence.
- **Never edit `site/`.** It is build output.
- Cross-links use `[Text](page-file.md#anchor-slug)`, the anchor being the lower-cased hyphenated heading.
- **Never link to a heading containing an apostrophe.** The site enables the `smarty` extension, which turns `'` into a curly `’`, and the resulting slug is not reliably what you would guess. `mkdocs build --strict` does not validate anchors, so a wrong one fails silently. Either link to an apostrophe-free heading or reword the heading.

## Facts verified against the shipped code

Use these exactly. They were read from the implementation, not inferred.

| Fact | Value |
|---|---|
| Recovery codes issued | **10** (`TwoFactorRecoveryCodes::CODE_COUNT`) |
| Recovery code format | Two groups of four characters, e.g. `A3F7-K29P`; letters A–Z and digits 2–7 only |
| Each code | Single use |
| Shown | Once, at the moment they are generated |
| Coverage segments | **Not set up**, **Never signed in**, **Suspended**, **Set up** |
| Segment precedence | Holding a secret wins over everything, so a suspended staff member who has enrolled appears under **Set up** |
| Headline | "N of M staff are set up" |
| Enrolment step headings | "Scan this code" (1) and "Enter the six digits" (2) |
| Staff card headings | "Recovery codes", "Remembered devices" |
| Removal page heading | "Remove two-factor authentication" |
| Mandate date | **1 January 2027** |

## File Structure

| File | Responsibility |
|---|---|
| `docs/two-factor-authentication.md` | The staff guide: the mandate, enrolling, recovery codes, remembered devices, losing your phone, passkeys. |
| `docs/two-factor-authentication-for-administrators.md` | **New.** Settings, the coverage screen, the dashboard prompt, per-staff actions. |
| `docs/logging-on-to-adam.md` | Two wrong passkey passages corrected; duplicated settings replaced with links. |
| `docs/passkey-authentication.md` | The prompt-versus-enrolment distinction added to one FAQ answer. |
| `mkdocs.yml` | `nav` entry for the new page, alphabetical. |
| `TODO.md` | One entry per screenshot needed. |

---

### Task 1: The staff page — the mandate and enrolment

**Files:**
- Modify: `docs/two-factor-authentication.md` lines 1-71

**Interfaces:**
- Produces: the anchors `#adding-two-factor-authentication-to-your-account` and `#supported-authenticator-apps`, which later tasks and other pages link to. Do not rename those headings.

- [ ] **Step 1: Replace the introduction's final paragraph**

Line 13 currently reads:

```markdown
***NB: 2FA is automatically enforced for all elevated privilege accounts. Schools can optionally require that all staff make use of 2FA. Any staff member can add 2FA to their account using voluntary enrolment.***
```

Replace it with:

```markdown
!!! warning
    From **1 January 2027**, two-factor authentication is required for every staff member who uses ADAM. You do not need to wait for that date — you can set it up now, and we would encourage you to. Once the requirement takes effect, ADAM will ask you to set it up the next time you sign in, and you will not be able to use ADAM until you have.

Two-factor authentication is already required for accounts with elevated privileges, whatever your school has chosen.
```

- [ ] **Step 2: Rewrite the enrolment section's opening**

Lines 35-45 currently distinguish "Compulsory Enrolment" from "Voluntary Enrolment". Replace everything from the `## Adding Two-Factor Authentication to your account` heading down to and including "ADAM will display the following screen:" with:

```markdown
## Adding Two-Factor Authentication to your account

First, [download and install an authenticator app](#supported-authenticator-apps) from your app store.

You can reach the setup page in two ways. If ADAM is waiting for you to set two-factor authentication up, it takes you there itself the next time you sign in. Otherwise, sign in as normal, click on the **Staff tab**, and then under the **Security Administration** heading click on **Manage your Two-Factor Authentication**.

The setup page asks you to do two things, in order.

### Step 1: Scan this code

ADAM shows a QR code alongside a written **Two-Factor Authentication Secret**. Scanning the code is simply a shortcut that saves you typing the secret into your phone by hand — the two carry the same information.
```

- [ ] **Step 3: Keep the corrupted-QR-code note, and place it correctly**

The existing italic note at line 49 warns that the example QR code is deliberately corrupted. Keep its substance, but move it below the screenshot and rewrite as an admonition, since the site has one for this purpose:

```markdown
!!! note
    The QR code in the picture above has been deliberately corrupted so that it cannot be scanned. Scan the code on **your own screen** — every account's code is different.
```

- [ ] **Step 4: Rewrite the scanning and confirmation steps**

Replace the text from "Now, open the two-factor authenticator app…" through "…you may need to re-scan the QR code." with:

```markdown
Open the authenticator app you installed, and choose its option to add a new account. The app will ask permission to use your camera so that it can scan the code. In the Google Authenticator app, for example, this is the **+** button at the bottom right of the screen.

Once the code has been scanned, the app lists the account and shows a six-digit number beneath it. That number changes every thirty seconds.

### Step 2: Enter the six digits

The last step tells ADAM that your app really did save the secret. Type the six digits currently shown in your app into the **Confirmation Code** box, and click on **Add Two-Factor Authentication Protection**.

If the digits were correct, ADAM confirms that two-factor authentication is now protecting your account, and shows you your recovery codes. **Do not leave that page without saving them** — see [Recovery codes](#recovery-codes) below.

If ADAM says the code was wrong, the most likely reason is that the six digits changed while you were typing. Try again with the number now showing in your app. If it fails repeatedly, see the [frequently asked questions](#frequently-asked-questions) below.
```

- [ ] **Step 5: Fix the menu path in "Removing Two-Factor Authentication"**

Line 75 says "visiting **Staff → Security Administration → Manage Two-Factor Authentication**". Replace that clause with: "clicking on the **Staff tab**, and then under the **Security Administration** heading clicking on **Manage your Two-Factor Authentication**".

Line 79's "Click on the **Remove Two-Factor Authentication** option at the bottom" stays accurate — the link is still at the bottom of the page — but the page it leads to is now headed **Remove two-factor authentication**. Add after line 79: "ADAM opens a page headed **Remove two-factor authentication**."

- [ ] **Step 6: Verify and commit**

```bash
cd ~/dev/adam-docs
grep -n "→" docs/two-factor-authentication.md
```

Expected: no matches in any section you rewrote. Some may remain in sections later tasks own; note which and leave them.

```bash
git add docs/two-factor-authentication.md
git commit -m "CHANGED: State the two-factor mandate and rewrite the enrolment walkthrough"
```

---

### Task 2: The staff page — recovery codes and remembered devices

**Files:**
- Modify: `docs/two-factor-authentication.md`, inserting two new `##` sections between "Adding Two-Factor Authentication to your account" and "Removing Two-Factor Authentication"

**Interfaces:**
- Produces: anchors `#recovery-codes` and `#remembered-devices`, linked from Task 1 and Task 3.

Both features are entirely absent from the manual today. This is new writing.

- [ ] **Step 1: Write the recovery-codes section**

(Outer fence is four backticks because the content itself contains a fenced block.)

````markdown
## Recovery codes

When you set up two-factor authentication, ADAM gives you **ten recovery codes**. Each one can be used once, in place of the six digits from your app, to sign in. They are what gets you back into ADAM when your phone is lost, broken, flat, or simply not with you.

A recovery code looks like this:

```
A3F7-K29P
```

They contain only the letters A to Z and the digits 2 to 7 — there is no letter O and no digit 0 or 1, so there is nothing to confuse.

!!! warning
    ADAM shows your recovery codes **once**, at the moment they are created, and never again. It cannot show them to you later, because it does not keep a readable copy — it stores only enough to check a code you type in. If you lose them, you can generate a fresh set, but the old ones stop working.

Print them, or download them, and keep them somewhere you can reach without your phone. A drawer at home is fine. A note on your desk beside the computer you sign in on is not — anyone who has your password and that note has your account.

### Using a recovery code

When ADAM asks for your six-digit code, use the option to sign in with a recovery code instead, and type one in. That code is then used up. Nine remain.

### Generating new codes

You can replace your codes at any time — if you have used most of them, or if you think someone else has seen them. Click on the **Staff tab**, then under the **Security Administration** heading click on **Manage your Two-Factor Authentication**, and choose to generate new recovery codes.

ADAM asks for your password and a code from your app first, to be sure it is you. Generating a new set **cancels every code in the old set**, so make sure you have saved the new ones before you close the page.
````

- [ ] **Step 2: Write the remembered-devices section**

```markdown
## Remembered devices

Depending on how your school has set ADAM up, it may not ask for your six-digit code every single time you sign in. It can instead remember the computer you are using, and skip the prompt for a while. Your school's administrator chooses this — see [how often ADAM asks for a code](two-factor-authentication-for-administrators.md#choosing-how-often-adam-asks-for-a-code).

Where that is in use, your two-factor authentication page shows a **Remembered devices** card telling you how many computers are currently trusted to skip the prompt.

!!! tip
    If you have signed in on a computer that is not yours — a shared office machine, a hotel, a friend's laptop — or if a laptop has been lost or stolen, use **Sign out all devices**. Every remembered computer is forgotten, and the next person to sign in on any of them has to enter a code.

Signing devices out does not remove two-factor authentication from your account and does not affect your recovery codes. It only means the code prompt comes back.

You may also see this card show nothing to sign out. That simply means no computer is currently being trusted — either because none has been, or because your school asks for a code at every sign-in.
```

- [ ] **Step 3: Verify the cross-link target exists**

The link in Step 2 points at a heading Task 4 creates. If Task 4 has not run yet, the link will be dead until it does. That is expected within the branch; confirm at the end of Task 6 that `mkdocs build --strict` reports no broken links.

- [ ] **Step 4: Commit**

```bash
git add docs/two-factor-authentication.md
git commit -m "NEW: Document recovery codes and remembered devices for staff"
```

---

### Task 3: The staff page — the FAQ and passkeys

**Files:**
- Modify: `docs/two-factor-authentication.md` lines 89-148 (the FAQ)

The three lost-phone answers currently say some version of "the short answer is that you can't". That is no longer true, and it is the answer a locked-out person reads first.

- [ ] **Step 1: Replace "How do I log in if I don't have my phone with me?"**

Replace the whole answer (currently lines 97-105) with:

```markdown
### How do I log in if I don’t have my phone with me?

Use one of your [recovery codes](#recovery-codes). When ADAM asks for the six digits, choose to sign in with a recovery code instead, and type one in. Each code works once.

If you have run out of codes, or never saved them, your ADAM administrator can [remove two-factor authentication from your account](#removing-two-factor-authentication-for-another-staff-member). You can then sign in with just your password — but if your school requires two-factor authentication, ADAM will ask you to set it up again straight away, and you will need your phone to do that.

If you are your school's ADAM administrator and you cannot sign in yourself, contact us for support. We will verify who you are before making any change.
```

- [ ] **Step 2: Replace "I have a new phone or don't have the App installed anymore. How do I log in?"**

```markdown
### I have a new phone or don’t have the App installed anymore. How do I log in?

Sign in with a [recovery code](#recovery-codes), then remove two-factor authentication from your account and set it up again on the new phone. Scanning the QR code on the new phone creates a new secret; the entry in your old app stops working, and you should delete it.
```

- [ ] **Step 3: Amend the "I removed the app" answer**

Keep the existing explanation and the `!!! warning` block at lines 117-118 — both are still accurate and still worth saying. Replace only its closing paragraph (line 122) with:

```markdown
If you lose your phone, or cannot generate a code for any other reason, sign in with a [recovery code](#recovery-codes). If you have none left, only your [ADAM administrator can remove the protection](#removing-two-factor-authentication-for-another-staff-member) from your account.
```

- [ ] **Step 4: Add a passkey question to the FAQ**

Insert as a new `###` immediately after the "I have two ADAM logins…" answer:

```markdown
### I sign in with a passkey. Do I still need two-factor authentication?

Yes. Signing in with a passkey means ADAM does not ask you for a six-digit code — the passkey is already a second factor, so a code on top of it would add nothing. But you still have to set two-factor authentication up.

The reason is that your password still works. A passkey is something you choose to use; it does not switch your password off. Anyone who obtains your password can still try to sign in with it, and the six-digit code is what stops them. See [Passkey Authentication](passkey-authentication.md#passkey-authentication) for more about passkeys.
```

- [ ] **Step 5: Fix the menu path in "Removing Two Factor Authentication for another staff member"**

Line 202 currently says "navigating to **Administration → Security Administration → Manage Two Factor Administration**" — arrows, and the menu name is wrong twice over. Replace that clause with: "clicking on the **Administration tab**, and then under the **Security Administration** heading clicking on **Manage Two-Factor Authentication for staff**".

Then add, immediately after that sentence:

```markdown
This screen is described in full in [Two-Factor Authentication for Administrators](two-factor-authentication-for-administrators.md#the-coverage-screen).
```

- [ ] **Step 6: Verify and commit**

```bash
grep -n "The short answer is that you can" docs/two-factor-authentication.md
grep -n "→" docs/two-factor-authentication.md
```

Expected: no matches for either.

```bash
git add docs/two-factor-authentication.md
git commit -m "CHANGED: Recovery codes come first in the lost-phone advice"
```

---

### Task 4: The administrator page

**Files:**
- Create: `docs/two-factor-authentication-for-administrators.md`
- Modify: `mkdocs.yml` (`nav`)
- Modify: `docs/two-factor-authentication.md` — remove the sections that move

**Interfaces:**
- Produces: anchors `#the-coverage-screen` and `#choosing-how-often-adam-asks-for-a-code`, linked from Tasks 2 and 3.

- [ ] **Step 1: Create the page with its opening and the mandate**

```markdown
# Two-Factor Authentication for Administrators

## Introduction

This page covers what an ADAM administrator needs to do about two-factor authentication: the settings that control it, how to see which staff have set it up, and the actions you can take on someone else's account.

Staff who want to set two-factor authentication up on their own account should read [Two-Factor Authentication](two-factor-authentication.md#two-factor-authentication) instead.

## The 2027 requirement

From **1 January 2027**, every staff member who uses ADAM must have two-factor authentication set up. This is not a setting you can decline — on that date ADAM begins asking any staff member who has not set it up to do so before they can continue.

You do not have to wait, and there is a good reason not to. A school that switches the requirement on early moves its staff over gradually, with help available and at a time of its choosing. A school that waits until the deadline moves every staff member on the same morning, which is usually the first morning of a term.

We would suggest, in order: train your staff, encourage them to set it up voluntarily, watch the [coverage screen](#the-coverage-screen) until the number of people left is small, help those people individually, and only then switch the requirement on.

## The settings

Click on the **Administration tab**, then under the **Site Settings** heading click on **Change the site settings**. Choose the **Security** tab and scroll down to the **Login Settings** heading.

![](assets/screenshots/two-factor-authentication/two-factor-authentication-11.png)

### Requiring two-factor authentication

Set **Two Factor Authentication Forced For Staff** to “Yes” to require it of every staff member now, ahead of the deadline.

Staff with elevated privileges are always required to use two-factor authentication, whatever this setting says.

### Choosing how often ADAM asks for a code

**Two-Factor Authentication Method** decides how often a staff member is asked for their six digits. There are three choices.

**At every login** is the most secure and the most tiring. Someone who signs in several times a day types a code every time.

**Once per computer per day** asks once each day on each computer somebody uses. This is the best balance for most schools.

**Once per computer** asks only when ADAM sees a computer it does not recognise. **Remember logged-in machines for** then decides how long that recognition lasts before ADAM asks again.

ADAM recognises a computer by a cookie stored in the browser. Clearing cookies, or using a different browser on the same computer, makes it a computer ADAM has not seen before.

Staff can see how many of their own computers are currently remembered, and sign them all out — useful if a laptop is lost. You can do the same on their behalf; see [managing another staff member](#managing-another-staff-member).

### The authentication window

**Two-Factor Authentication Window** decides how much clock difference ADAM tolerates between its own time and the phone generating the code. Each window is thirty seconds, and the default of 2 accepts codes from two windows either side of the current time.

Raising it to 3 makes a code usable for about three minutes, which is less secure — a code seen over someone's shoulder stays valid for longer. Lowering it to 1 is the most secure and the least forgiving of a phone whose clock is drifting.

If a lot of staff suddenly cannot enrol, suspect the server's clock rather than this setting.
```

- [ ] **Step 2: Write the coverage-screen section**

```markdown
## The coverage screen

Click on the **Administration tab**, then under the **Security Administration** heading click on **Manage Two-Factor Authentication for staff**.

The screen opens with a single line telling you where the school stands — for example, “**34 of 51 staff are set up**”. Below it, every current staff member appears in one of four tables.

**Set up** — they hold a second factor. Nothing is needed from them.

**Not set up** — they have signed in before, they can sign in now, and they have not set two-factor authentication up. This is the list that matters: these are the people who will be stopped at the door when the requirement takes effect.

**Never signed in** — an account exists but has never been used. Setting up two-factor authentication is part of their first sign-in, so there is usually nothing to chase here.

**Suspended** — the account cannot sign in at all. They are shown so that the totals account for everybody, not because anything is expected of them.

!!! note
    A staff member who is suspended but has already set two-factor authentication up appears under **Set up**, not under **Suspended**. Holding a second factor takes precedence over every other state, so the number in the headline is always exactly the length of the **Set up** table.

## The reminder on your dashboard

Staff who have not set two-factor authentication up see a card on their ADAM dashboard inviting them to. As 1 January 2027 approaches the card's wording becomes more insistent, and after the date has passed it says so.

The card disappears as soon as they enrol. There is nothing to configure, and a staff member cannot dismiss it permanently — it is a reminder of something that is about to become compulsory, not a suggestion.
```

- [ ] **Step 3: Write the per-staff actions section**

```markdown
## Managing another staff member

Both actions below appear next to a staff member's name in the **Set up** table on the [coverage screen](#the-coverage-screen).

### Removing someone's two-factor authentication

Use this when somebody cannot get in and has no recovery codes left.

ADAM asks you to confirm your own password and your own six-digit code first. This is deliberate: the list in front of you is every staff member at the school, and a stranger sitting at an unattended administrator's desk should not be able to work down it.

!!! warning
    Removing two-factor authentication does not remove anything from the staff member's phone. When they set it up again they must scan a new QR code, and they should delete the old entry from their authenticator app first — the old entry's codes will never work again.

If your school requires two-factor authentication, the staff member is asked to set it up again the moment they next sign in.

### Signing out their remembered devices

Use this when a staff member's laptop or phone has been lost or stolen and you want every computer ADAM was trusting for them to be forgotten straight away.

Every remembered computer is forgotten, and the next sign-in from each asks for a code. Their second factor itself is untouched, and so are their recovery codes.

ADAM emails the staff member to tell them this happened, so that they are not left wondering why they are suddenly being asked for a code again. If there was nothing to sign out, no email is sent.
```

- [ ] **Step 4: Remove the moved sections from the staff page**

Delete these from `docs/two-factor-authentication.md`, in full:

- `## Setting up your ADAM server for Two-Factor Authentication` and everything under it, down to but not including `## Removing Two Factor Authentication for another staff member`. That covers the settings, the authentication windows, forced use, and the OTP-frequency sub-sections.

Keep `## Removing Two Factor Authentication for another staff member` where it is — Task 3 has already pointed it at the new page — and keep `## Troubleshooting 2FA and OTPs`, which is advice for anybody.

Note that `two-factor-authentication-11.png` is now referenced from the administrator page instead. The image file does not move; only the reference does.

- [ ] **Step 5: Add the page to the navigation**

In `mkdocs.yml`, the `nav` list is flat and ordered alphabetically by display title. Insert immediately after the existing Two-Factor Authentication entry:

```yaml
  - Two-Factor Authentication: two-factor-authentication.md
  - Two-Factor Authentication for Administrators: two-factor-authentication-for-administrators.md
  - Updating ADAM: updating-adam.md
```

- [ ] **Step 6: Verify and commit**

```bash
cd ~/dev/adam-docs
grep -n "Forced For Staff" docs/two-factor-authentication.md
```
Expected: no matches — that content now lives only on the administrator page.

```bash
git add docs/two-factor-authentication-for-administrators.md docs/two-factor-authentication.md mkdocs.yml
git commit -m "NEW: A two-factor authentication page for administrators"
```

---

### Task 5: Correcting the other two pages

**Files:**
- Modify: `docs/logging-on-to-adam.md` lines 22, 67-71, 124-140
- Modify: `docs/passkey-authentication.md` lines 88-92

This is the task that removes the statements contradicting how ADAM behaves.

- [ ] **Step 1: Correct `logging-on-to-adam.md` line 22**

It currently reads:

```markdown
A successful passkey login satisfies the Two-Factor Authentication requirement on its own — the user is not asked for a one-time PIN as well.
```

Replace with:

```markdown
Signing in with a passkey does not also ask for a one-time PIN — the passkey is itself a second factor. It does not, however, excuse the user from setting two-factor authentication up; see [Passkeys and Two-Factor Authentication](#passkeys-and-two-factor-authentication) below.
```

- [ ] **Step 2: Rewrite the "Passkeys and Two-Factor Authentication" section**

Replace the whole section (lines 67-71) with:

```markdown
### Passkeys and Two-Factor Authentication

A passkey is itself a strong second factor — the device holding it, plus the biometric or PIN that unlocks it — so a user who signs in with a passkey is not asked for a one-time PIN as well. That remains true when **Two Factor Authentication Forced for Staff** is set to “Yes”.

What a passkey does **not** do is excuse a staff member from setting two-factor authentication up. Their password still works, and anyone who obtains it can still try to use it; the one-time PIN is what stops them. A staff member who signs in with a passkey but has not set up two-factor authentication will be asked to do so, exactly like anyone else.

Users signing in with a username and password continue to be asked for a one-time PIN as before.
```

- [ ] **Step 3: Replace the duplicated settings descriptions**

Lines 124-140 describe **Remember logged-in machines**, the OTP frequency options and **Two Factor Authentication Forced for Staff** — all of which the administrator page now covers properly. Replace those descriptions with a short pointer, keeping any surrounding login-settings content that is not about two-factor authentication:

```markdown
The **Remember logged-in machines** setting stores a long-term cookie on a computer so that ADAM can recognise it on a later visit. It works together with the two-factor authentication settings, and both are described in [Two-Factor Authentication for Administrators](two-factor-authentication-for-administrators.md#the-settings).
```

Read the surrounding lines before cutting. If a sentence there covers something other than two-factor authentication, keep it.

- [ ] **Step 4: Amend the passkey FAQ answer**

`docs/passkey-authentication.md` lines 88-92 currently end with the comparison between passkeys and 2FA. Append a paragraph to that answer:

```markdown
The two are not alternatives, though. Staff are required to set up two-factor authentication whether or not they use a passkey, because the account's password still works and still needs a second factor protecting it. Using a passkey means you are not asked for a one-time PIN when you sign in that way.
```

- [ ] **Step 5: Verify and commit**

```bash
grep -rn "unaffected by passkey enrolment\|satisfies the Two-Factor Authentication requirement" docs/
```
Expected: no matches anywhere.

```bash
git add docs/logging-on-to-adam.md docs/passkey-authentication.md
git commit -m "FIXED: Passkeys waive the code prompt, not the requirement to enrol"
```

---

### Task 6: Screenshots and the build

**Files:**
- Modify: `TODO.md`
- No documentation prose changes

- [ ] **Step 1: Add the screenshot entries**

Append to `TODO.md`, following that file's existing format exactly — a `##` heading naming the page and its file, a short paragraph of context, then a `###` entry per image giving the path, how to reach the screen, what to frame, and what the data should look like. Read an existing entry first and match it.

Entries needed:

1. `two-factor-authentication-12.png` — the rebuilt setup page, both steps visible, replacing `-04.png`.
2. `two-factor-authentication-13.png` — the **Confirmation Code** box in step 2, replacing `-06.png`.
3. `two-factor-authentication-14.png` — the recovery codes as shown once after enrolling, replacing `-07.png` as the success screen.
4. `two-factor-authentication-15.png` — the **Recovery codes** and **Remembered devices** cards side by side on the management page.
5. `two-factor-authentication-for-administrators-01.png` — the coverage screen, headline and all four tables.
6. `two-factor-authentication-for-administrators-02.png` — the dashboard reminder card.

State in each entry that `-04.png`, `-06.png` and `-07.png` are to be deleted once their replacements are in place, per that file's standing rule. Also say that `-05.png` (the phone-side app) and `-08.png`/`-09.png` (the removal flow) should be checked against the rebuilt pages and listed only if they no longer match.

**Recovery codes are secrets.** The entry for `-14.png` must say that the codes on screen are a real generated set for the demonstration account and must be regenerated immediately after the capture, so that what is published is no longer usable.

- [ ] **Step 2: Build the site and check every link**

```bash
cd ~/dev/adam-docs
mkdocs build --strict
```

`--strict` turns warnings into errors, so a broken internal link or a missing nav file fails the build. Fix anything it reports. If `mkdocs` is not on the path, check `requirements.txt` and the repo's README for how the site is normally built, and say in your report what you ran.

- [ ] **Step 3: Do not commit `site/`**

`mkdocs build` writes to `site/`. Check whether that directory is tracked:

```bash
git status --short site/ | head
```

If it shows modifications, do **not** stage them unless `site/` is genuinely tracked in this repo and updated by hand elsewhere — check `git log --oneline -3 -- site/` to see whether generated output is normally committed, and say what you found in your report.

- [ ] **Step 4: Commit**

```bash
git add TODO.md
git commit -m "NEW: Screenshots needed for the two-factor documentation"
```

---

## Out of scope, deliberately

- **Taking the screenshots.** They need a demonstration tenant and a browser.
- **`docs/logging-on-to-adam-a-guide-for-parents.md`.** The requirement is staff-only and that guide carries no two-factor content.
- **The announcement to schools.** A separate deliverable, drafted and unsent.
- **Families and pupils.** A later phase of the programme.
- **Rewriting pages that merely mention logging in.** Only the four files named here are touched.
