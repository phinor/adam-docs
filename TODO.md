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

## Reporting Period Administration (`docs/reporting-period-administration.md`)

The time frame grid now carries a **Markbook Editing** line, sitting between **Markbook Entry** and
**Markbook Embargo**. The existing captures on the page pre-date it, so the grid in the manual is
one line short of what an administrator will see.

### 1. Re-capture `reporting-period-administration-09.png` — the time frame grid

**Reporting tab → Reporting Administration → Edit reporting period time frames**, then choose a
reporting period. Capture the whole grid, keeping the existing filename and crop, so that the new
**Markbook Editing** row is visible in its place.

Set the demonstration school up first so the row illustrates the point: give **Markbook Entry** a
window that has already closed, and **Markbook Editing** a window that runs on for a further week
after it. That way the picture shows the two-stage close-off the text describes rather than an
empty line.

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

### 2. `parent-and-pupil-portal-10.png` — the three settings together

**Administration → Site Administration → Edit site settings**, the **Pupils & Families** tab,
scrolled to the **Widgets** heading. All three birthday settings must be in shot: **Birthdays
visible in the portal**, **Show photographs in the portal birthday widget** and **Names in the
portal birthday widget**. Leave photographs on **No** and names on **First name and surname
initial**, so the image shows the defaults a school starts from rather than a configuration that
happens to suit the screenshot.

### 3. `parent-and-pupil-portal-11.png` — the list as a parent sees it

**Families → Security → Login as a family** for a demonstration family with more than one child, so
that the birthday card can be seen sitting *below* the children's cards — that placement is the
point of the image and is easy to lose by cropping too tightly. Frame the foot of the portal front
page: the last child's card, the **Family** and **Security** menu, and the **Today's Birthdays**
card. Photographs off and names abbreviated, matching the defaults in image 2.

If no demonstration pupil has a birthday on the day of capture, change one pupil's date of birth on
the demonstration school to today rather than waiting — but pick a pupil in the same family's scope,
and set it back afterwards.

## Heads of Subject (`docs/subjects.md`)

**The manual does not mention heads of subject anywhere.** Searching the whole of `docs/` for "head
of subject", "heads of subject" or "headed subject" returns nothing, yet the feature drives eight
permissions and is a prerequisite for the [mark book editing
window](docs/reporting-period-administration.md#markbook-editing) that was documented alongside
this entry. Support has already seen the consequence of the gap: "the HOD says they still can't edit
marks", when in fact only one of the two halves had been set up.

This needs a new **Heads of Subject** section on the **Subjects** page, most naturally after
*Editing a Subject* and before *Changing the Order of Subjects*.

### What the section has to say

**The two halves.** This is the whole point of the section, so lead with it. A head-of-subject
permission and a head-of-subject assignment are both required, and **either one on its own does
nothing at all and gives no error**. The permission says *what* a subject head may do; the
assignment says *which* subjects they may do it in. ADAM now shows a warning when heads are saved
who hold none of these permissions, but it still saves the assignment, because granting the
permissions afterwards is a perfectly normal order of work.

**How to assign them.** From the **Subjects** tab, under the **Subject Administration** heading,
click **Edit the subjects**, then click the **heads** action next to the subject concerned. The
**Manage Heads of Subject** screen lets you pick one or more staff members under **Staff Members**;
click **Save**. Current heads are listed in the **Head(s)** column back on the subject list. The
person doing this needs the **Manage Head of Subject assignments** permission.

**The permissions that the assignment scopes.** All eight are worth listing, with the tab and heading
each is found under, since they are scattered across the permission screen:

- **Add classes within headed subjects** and **Edit classes within headed subjects** — Class Admin
  tab, Classes and Registrations heading.
- **Add assessments for classes in headed subjects**, **Edit assessment results for headed
  subjects** and **Edit assessment results for headed subjects during the mark book editing
  window** — Assessments tab, Class Assessments heading.
- **Enter report comments for headed subjects** and **Edit report marks for headed subjects** —
  Reporting Admin tab, Reports heading.
- **Manage aggregated result calculations from subjects taught** — Reporting Admin tab, Aggregated
  Result Calculations heading.

### Cross-links to add once the section exists

- `docs/mark-book-administration.md`, in *When the Mark Book Closes* — the note about a head of
  department needing both the permission and the assignment should link to the new section rather
  than restating it.
- `docs/reporting-period-administration.md`, in *Markbook Editing* — same, for the second of the two
  permissions listed there.

### One thing to check with development first

The last permission in the list above, **Manage aggregated result calculations from subjects
taught**, is scoped by the head-of-subject assignment in the code like the other seven, but its
on-screen description says "for subjects that they teach" rather than *head*. Either the wording or
the behaviour is wrong. Do not paper over it in the manual — ask which was intended, and document
whichever answer comes back.

### Screenshots this section will need

Capture these against the demonstration school at the same time as writing the section, into
`docs/assets/screenshots/subjects/`:

1. The **Manage Heads of Subject** screen for a subject that already has two heads, showing the
   **Staff Members** picker with both selected and the **Save** button.
2. The subject list with the **Head(s)** column populated, and the **heads** action visible on the
   row, so the reader can see where the action lives.
