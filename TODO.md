# TODO: Screenshots to be Captured

These are screenshots that the manual needs but does not yet have, or has in a form that no longer
matches ADAM. Each entry says which page the image belongs to, how to get to the screen, what to
frame, and what the data on screen should look like.

**Remove an entry from this file as soon as it is done** — a completed task must not be left here.
The whole file can go once it is empty.

Two standing rules from [`CONTRIBUTING.md`](CONTRIBUTING.md) apply to everything below:

- Capture against the **demonstration school**, never a live site. No real pupil, family or staff
  information may appear.
- Save each image at the given path under `docs/assets/screenshots/`, and add the `![](...)`
  reference to the page at the point described.

Most pupil screenshots in the manual use the demo pupil **Brandon Dayne Jarred Clark** (admin number
48619), but the Profile Overview Layouts captures were taken against **Riley Anderson** (admin
number 99726). Reuse Riley Anderson on that page and Brandon Clark elsewhere, so that each page at
least reads as one continuous example.

---

## Profile Overview Layouts (`docs/profile-overview-customisation.md`)

The demonstration school now has three pupil layouts — **Default** (the default), **Admin Layout**
and **Medical** — and they appear in the captures already in the manual. Use the same three for
anything below.

### 1. `profile-overview-customisation-15.png` — recommending a layout

From the catalogue, click on the action that chooses which staff members should be given a layout,
next to **Admin Layout**. Capture the heading, the sentence explaining that these staff members will
see this layout unless they pick another, and the **Staff members** selector with three or four demo
staff members already selected, so that it is clear the control holds several names.

Goes in *Recommending a Layout to Staff*.

**Check the label while you are there.** The page describes this action as **recommend**, but
`profile-overview-customisation-13.png` shows the catalogue offering a **people** button, and a
**see who is using which layout** link above the table that the page does not mention at all. If
**recommend** is no longer the label, the *Managing the Available Layouts* action list and the
*Recommending a Layout to Staff* heading and text need correcting to match.

---

## Two-Factor Authentication (`docs/two-factor-authentication.md`,
`docs/two-factor-authentication-for-administrators.md`)

`two-factor-authentication-05.png` (the phone-side authenticator app screenshot) has been checked
against the rebuilt page and still matches. `-07.png` and `-08.png` were the same file — the old
management screen — and have been deleted; the *Removing Two-Factor Authentication* section now uses
`-15.png`.

### 2. `two-factor-authentication-09.png` — re-capture the removal confirmation

The existing image no longer matches the page. *Removing Two-Factor Authentication* says ADAM opens
a page headed **Remove two-factor authentication**; the image shows the old **Manage Two-Factor
Authentication** heading and the older styling. Re-capture the password confirmation step, keeping
the same filename, and correct the page's wording if the heading turns out to differ.

### 3. `two-factor-authentication-for-administrators-01.png` — the coverage screen

New page, new screenshot folder: `docs/assets/screenshots/two-factor-authentication-for-administrators/`.

Click on the **Administration tab**, then under the **Security Administration** heading click on
**Manage Two-Factor Authentication for staff**. Capture the headline line ("**N of M staff are set
up**") and all four tables, which the screen renders in this order: **Not set up**, **Never signed
in**, **Suspended**, **Set up**. Have at least one demo staff member in each so that none of the
four reads as empty.

Goes in *The coverage screen*.

### 4. `two-factor-authentication-for-administrators-02.png` — the dashboard reminder card

Sign in as a demo staff member who has not yet set up two-factor authentication, and capture the
reminder card on their ADAM dashboard.

**Set Two Factor Authentication Forced For Staff to "No" on the demonstration school first.** Once
enrolment is actually required of someone, ADAM sends them straight to the setup page and they never
reach a dashboard — so with the setting on there is no card to photograph.

Goes in *The reminder on your dashboard*.
