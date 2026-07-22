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

The existing pupil screenshots use the demo pupil **Brandon Dayne Jarred Clark** (admin number
48619). Reuse that pupil wherever a pupil is needed, so that the manual reads as one continuous
example.

---

## Profile Overview Layouts (`docs/profile-overview-customisation.md`)

The layouts feature replaced the old per-user overview customisation, so this page was rewritten and
now has almost no illustrations. Three of the old images show screens that no longer exist and are
**no longer referenced by any page**: `profile-overview-customisation-01.png`, `-04.png` and
`-06.png`. `-05.png` was already unreferenced before the rewrite. Delete all four once their
replacements below are in place.

Before capturing, the demo school needs a small, believable catalogue of pupil layouts — three or
four is enough, and they should look like layouts a school would really build. Suggested names and
descriptions:

- **School Default** — "The standard pupil overview." *(this one is the default)*
- **Register Teacher** — "Contact details, allergies and today's absentees."
- **Subject Teacher** — "Marks and academic progress, with the photograph."
- **Office** — "Full pupil and family details for the front desk."

Give **Register Teacher** a handful of staff members under **recommend**, and set the demo user's own
choice to **Subject Teacher**, so that the counts and the "you are using…" wording in the captures
below are not all zeros or all identical.

### 1. `profile-overview-customisation-11.png` — the "change this layout" link

Replaces the old `-01.png`, which shows the removed "edit this page" link.

Open a pupil's profile: click on the **Pupils tab**, find the demo pupil, and open their
**Overview**. Frame the top of the page: the **Overview** heading and the full row of action links
beneath it, including **edit pupil information**, **print detail update form**, **email detail update
form link** and — the point of the image — **change this layout**. Include just enough of the first
blocks below the links to show that this is the overview page. Same crop as the old `-01.png`.

Goes in the introduction, immediately after the opening paragraphs.

### 2. `profile-overview-customisation-12.png` — the layout chooser

From that page, click on **change this layout**. Capture the whole content area: the **Choose your
Pupil Overview layout** heading, the sentence saying which layout you are on and why, the radio list
of layouts with their descriptions and **preview** links, the **Use this layout** button, and the
**use the recommended layout** and **edit the available layouts** links below it.

Sign in as a user who has chosen a layout for themselves, so that the sentence reads "You are using a
layout you chose yourself" and the **use the recommended layout** link is present — otherwise that
link is hidden and the image will not match the text.

Goes in *Choosing Your Own Layout*.

### 3. `profile-overview-customisation-13.png` — the layout catalogue

From the chooser, click on **edit the available layouts**. Capture the **Pupil Overview Layouts**
heading, the sentence about layouts being safe to give to anyone, the **create a new layout** link,
and the whole table — the **Layout**, **Description**, **Blocks**, **People** and action columns.

The image is doing two jobs, so check both before capturing: the default layout must show
**(default)** after its name and must be missing the **make default** and **delete** actions, and at
least one other row must show a non-zero **People** count.

Goes in *Managing the Available Layouts*, above the list of actions.

### 4. `profile-overview-customisation-07.png` — the block editor (**re-capture, replacing the existing file**)

The existing image is still correct for the individual block controls, but its top is wrong: it shows
the old **Edit an Overview Page / Pupil Overview Page / Default Overview Page** headings and the old
sentence about users who have not customised their page. None of that exists any more.

Re-capture it: from the catalogue, click **edit** on the **Register Teacher** layout. Frame the
**Register Teacher** heading, the **Pupil Overview Layout** sub-heading, the **preview this layout**
and **back to all layouts** links, the **Name** and **Description** fields, the **Add another block**
link, and the first two blocks — as before, one a **Widget** block set to **Pupil Photograph**, the
other a **Field list** block headed *Pupil Information* — so that both kinds of block are visible.

Keep the existing filename so the reference in *Editing the Blocks* keeps working.

### 5. `profile-overview-customisation-14.png` — a layout preview

From the block editor, click on **preview this layout** and choose the demo pupil. Capture the
**Preview: Register Teacher** heading, the **preview against someone else** link, and the rendered
blocks below — enough of them to show that this is a real overview page and not the editor.

Goes in *Previewing a Layout*.

### 6. `profile-overview-customisation-15.png` — recommending a layout

From the catalogue, click on **recommend** next to **Register Teacher**. Capture the **Recommend:
Register Teacher** heading, the sentence explaining that these staff members will see this layout
unless they pick another, and the **Staff members** selector with three or four demo staff members
already selected, so that it is clear the control holds several names.

Goes in *Recommending a Layout to Staff*.

### 7. `profile-overview-customisation-16.png` — the Overview privileges

Replaces the old `-04.png`, which shows the two removed `customise_*` privileges.

Click on the **Administration tab**, then under the **Staff Groups heading** click on **Manage staff
groups**, click on the **privileges** link next to a group, and open the **Pupil Admin tab**. Scroll
to the **Overview heading**. Frame that heading and the two privileges
beneath it — **Manage Pupil Overview layouts** and **Choose own Pupil Overview layout** — with their
descriptions, cropped the same way as the old `-04.png`. Tick **Choose own Pupil Overview layout**
and leave **Manage Pupil Overview layouts** unticked, matching the advice in the text that most
teachers get only the first.

Goes in *Assigning the Privileges to Staff*.

---

## Managing Scratch List Fields (`docs/database-field-management.md`)

The *Restoring the Default Settings* section is new and has no illustrations.

### 8. `database-field-management-08.png` — the per-field Reset button

Click on the **Administration tab**, then under the **Database Administration heading** click on
**Manage scratch list fields**, choose **Pupil** and click on **edit**.

Capture three or four consecutive rows of the field table, full width — the drag handle and sort
order, the **Field Description**, the **Category**, the **enabled / sensitive / hidden** checkboxes,
and the **Reset** button at the end of each row. The **Reset** button is the subject of the image, so
do not crop it off; include the table headings above the rows for context.

Goes in *Restoring the Default Settings*, with the bullet about resetting a single field.

### 9. `database-field-management-09.png` — Restore all defaults

The bottom of the same screen: the **Save** button and the **Restore all defaults** link beneath it.
A narrow strip is enough.

If it captures well, prefer a version showing the confirmation dialog that the link raises — titled
**Restore all defaults**, asking "Discard every customisation for these fields and restore the
defaults?" — since the text tells the reader to expect it.

Goes in *Restoring the Default Settings*, with the bullet about restoring every field at once.
