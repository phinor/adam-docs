# TODO: Outstanding Documentation Work

Most of this file is **screenshots** that the manual needs but does not yet have, or has in a form
that no longer matches ADAM. Each entry says which page the image belongs to, how to get to the
screen, what to frame, and what the data on screen should look like.

The last section, [Missing Written Content](#missing-written-content), is for features that the
manual does not cover at all and that need a page or a section written first.

**Remove an entry from this file as soon as it is done** — a completed task must not be left here.
The whole file can go once it is empty.

Two standing rules from [`CONTRIBUTING.md`](CONTRIBUTING.md) apply to every screenshot below:

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

### 1. The **Move selected to:** control — still needs a picture

`profile-overview-customisation-15.png` is captured and in place. It shows the **Pupil Overview: who
uses what** heading, the sentence about moving someone, the table, and all three **How** states —
**own choice**, **assigned** and **following the default** — which was the point of it.

What it does not show is the **Move selected to:** control and its **Move selected** button. Those sit
at the foot of the screen, and with 97 staff on the demonstration school and no filter on the list,
they are some 3,900px below the heading. One image spanning both would be an unreadable strip.

**A decision is needed** rather than another capture attempt: either add a second image (say
`profile-overview-customisation-17.png`) framing just the **Move selected to:** control at the bottom,
placed in *Seeing and Changing Who Uses What* after the paragraph that describes it, or accept that
the control is adequately described in prose and drop the requirement.

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

---

## Messaging Centre — audiences and the admissions filter (`docs/messaging-centre.md`)

Two new sections were written without pictures: *Choosing an audience* and *Messaging applicants and
their parents*. Neither is unreadable as it stands — both are lists and steps rather than screens
that need pointing at — but the manual illustrates every other stage of the messaging flow, so these
two look bare by comparison.

The existing captures on the page run `messaging-centre-02.png` (choosing a module) straight to
`-03.png` (choosing a subject), which is exactly the step the *Choosing an audience* section now
describes. Number the new images from `-20.png` upward rather than renumbering the existing set.

### 1. The audience list — `messaging-centre-20.png`

**Admissions tab → Messaging and Communications → Messaging Centre for Admissions**, or open the
Messaging Centre from any tab and choose the Email module. The screen shows the sentence *"Please
select an audience to send your email to:"* — the wording names the module, so an SMS module reads
*"...your SMS to:"* — followed by the audiences the signed-in user may use.

Capture it as a user holding **all** of the messaging permissions, so that every audience appears —
**Pupils by class**, **Pupils by grade**, **Pupils by filter**, **Staff**, **Admissions**,
**Admissions by filter**, **Alumni** and **Leavers**. A shorter list would be misleading, because the
text explains that the list varies with permissions. Frame the heading and the full list of links.

Place it in *Choosing an audience*, immediately after the sentence quoting the prompt.

### 2. The admissions filter builder — `messaging-centre-21.png`

**Admissions tab → Messaging and Communications → Messaging Centre for Admissions (by filter)**.

Build a filter that matches a believable handful of demonstration applicants — a criterion or two, not
an empty form and not the whole intake — and click **Update the filter** so the capture shows the
result. Frame the criteria table, the **Update the filter** button, the sentence reporting how many
records match, the names listed beneath it, and the **Next** button at the foot with its count.

That single image carries the whole section: the builder, the running count, the name check and the
way out. Place it in *By filter*, after the paragraph that ends "...as many times as you need."

!!! note for whoever captures this
    The demonstration school must have applicants with enough variety to make a meaningful filter —
    check that **Admissions → Lists and Labels → Admissions scratch list using filters** returns rows
    before setting up the shot. If it does not, the demonstration data needs seeding first and that
    is the blocker, not the screenshot.

---

# Missing Written Content

## Parent and Pupil Portal — Today's Birthdays (`docs/parent-and-pupil-portal.md`)

The new **Today's Birthdays** section is written but has no images. It needed three: the permission,
the settings, and the result as a parent actually sees it. The permission is captured; the settings
and the parent's-eye view remain. The feature is off by default on the demonstration school, so each
capture needs setting up first.

Image 1 was captured against the **Full Access** pupil login group, chosen because it was the only
login group with any pupils assigned. Use the same group for images 2 and 3 — item 3 needs a parent
login, so keeping the group consistent across all three matters.

Grant **View birthdays** to the login group that the demonstration families use, and set
**Birthdays visible in the portal** to **All pupils in the school** before capturing — at the
default class scope, a demonstration login will usually see nobody and the section will not render
at all.

### 2. `parent-and-pupil-portal-11.png` — the list as a parent sees it

**Families → Security → Login as a family** for a demonstration family with more than one child, so
that the birthday card can be seen sitting *below* the children's cards — that placement is the
point of the image and is easy to lose by cropping too tightly. Frame the foot of the portal front
page: the last child's card, the **Family** and **Security** menu, and the **Today's Birthdays**
card. Photographs off and names abbreviated, matching the defaults in image 2.

**Blocked on demonstration data, and this is the setup it needs first.** No family on the
demonstration school currently satisfies the brief. `pupil_login_privileges` puts only three pupils in
the **Full Access** group, and just one of them, **Riley Anderson** (pupil 4753, family 1902), is a
current pupil — an only child. Every other family, including the two-child families, gets *"your
profile has not been granted access to any pupil information"* on logging in, so there are no
children's cards for the birthday card to sit below.

Pick a family with two current children — **de Villiers** (family 3090: Owen and Sheryl) is one — and
put **both** children into the **Full Access** pupil login group, so the portal renders two cards.
Keep to Full Access, so all three birthday images stay on one group.

The settings side is already done and needs no repeating: **Birthdays visible in the portal** is
**All pupils in the school**, photographs are **No**, names are **First name and surname initial**.
Two pupils genuinely have a birthday today, so no date of birth needs moving — but note that the two
with birthdays are **Yasmin Butcher** and **Coral Till**, in other families, which is exactly why the
school-wide scope matters for this image.

## Staff detail updates — the undo is still missing

The two faults found while capturing `staff-information-23.png` on 2026-08-26 are fixed in the
application, and this page is written against the fixed behaviour:

- staff who lack `staff_edit_own` are no longer offered on **Request staff detail updates**, and a
  note above the list accounts for them; and
- the ADAM home page no longer redirects a staff member to a prompt that would refuse them, so a
  request made before the permission existed simply waits instead of breaking the page.

---

## Heads of Subject — one question for development

The **Heads of Subject** section is now written, on `docs/subjects.md` between *Editing a Subject* and
*Changing the Order of Subjects*. The cross-links from `docs/mark-book-administration.md` and
`docs/reporting-period-administration.md` now point at it instead of restating the two-halves rule,
and both screenshots are captured and placed. One thing is left.

### Ask development about `rep_aggregated_subject`

This entry previously assumed **Manage aggregated result calculations from subjects taught** was
scoped by the head-of-subject assignment like the other seven permissions, and that its description
was wrong. **Reading the code says the opposite.**

`AggregatedCalculationsController` scopes it with `Subjects::isCurrentTeacher` and contains no
head-of-subject check anywhere, so the behaviour matches the on-screen description: it is about
subjects **taught**, not subjects **headed**. The section as written says so.

The misalignment is elsewhere: `SubjectHeadController::SUBJECT_SCOPED_PRIVILEGES` lists
`rep_aggregated_subject` alongside the seven genuinely head-scoped permissions, under a docblock
saying every entry "is scoped by the `subject_heads` table". That has a visible consequence — the
warning shown when saving a head who holds none of the head-of-subject permissions counts this one as
though it qualified, so a staff member holding only this permission is assigned as a head with no
warning, and still gains nothing from the assignment.

**Ask which is intended.** If the permission is meant to be head-scoped, the controller needs the
check and the manual's note about it should be removed. If it is meant to stay teach-scoped, it should
come out of `SUBJECT_SCOPED_PRIVILEGES` so the warning stops counting it. Either way the manual needs
re-checking against the answer.
