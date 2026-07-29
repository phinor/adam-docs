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

### 1. `profile-overview-customisation-15.png` — who is using which layout

The page now describes the roster that replaced recommendations, and has no picture of it.

From the catalogue, click on **see who is using which layout**. Capture the **Pupil Overview: who
uses what** heading, the sentence about moving someone replacing whatever they had, the table —
**Staff member**, **Layout** and **How** — and the **Move selected to:** control with its
**Move selected** button at the bottom.

The **How** column is the point of the image, so make sure the demo school has staff in more than
one state before capturing: at least one **own choice**, one **assigned**, and one **following the
default**.

Goes in *Seeing and Changing Who Uses What*.

### 2. `profile-overview-customisation-16.png` — re-capture the Overview privileges

The capture in the manual is one build out of date: it describes **Manage Pupil Overview layouts**
as letting a user "create, edit, delete and recommend the layouts", but recommendations are gone and
the privilege now reads "create, edit, delete and **assign** the layouts". Re-capture the same crop,
keeping the filename, once the demonstration server is on a build with the corrected wording.

While you are there, tick **Choose own Pupil Overview layout** and leave **Manage Pupil Overview
layouts** unticked, matching the advice in the text that most teachers get only the first.

---

## Two-Factor Authentication (`docs/two-factor-authentication.md`,
`docs/two-factor-authentication-for-administrators.md`)

`two-factor-authentication-05.png` (the phone-side authenticator app screenshot) has been checked
against the rebuilt page and still matches. `-07.png` and `-08.png` were the same file — the old
management screen — and have been deleted; the *Removing Two-Factor Authentication* section now uses
`-15.png`.

*The reminder on your dashboard* is deliberately without an illustration. The card could not be made
to appear on the demonstration server, and the section reads perfectly well without a picture, so
nothing is outstanding there.
