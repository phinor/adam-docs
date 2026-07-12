# Contributing to the ADAM Documentation

Thank you for helping to improve the ADAM documentation! This is a living
document, and the people who use ADAM every day are often the best placed to
spot a confusing sentence, a step that has changed, or a topic that is missing.

**You do not need to be a programmer to contribute.** You do not need to
install anything on your computer. If you can use a web browser and write in
plain English, you can help. This guide walks you through it, one screen at a
time.

## The quickest way: just tell us

If you would rather not edit anything yourself, that is completely fine. You
have two easy options:

- **Email us.** Send your suggestion to
  [help@adam.co.za](mailto:help@adam.co.za). Tell us which page you are looking
  at (the page title or its web address is perfect) and what you think should
  change.
- **Open an "issue" on GitHub.** An issue is simply a note asking for something
  to be fixed or added. Go to the
  [Issues page](https://github.com/phinor/adam-docs/issues), click the green
  **New issue** button, give it a short title, describe the problem, and click
  **Submit new issue**. (You will need a free GitHub account — see below.)

Either way, someone will pick it up. This is often the best choice for
reporting a problem when you are not sure what the correct wording should be.

## Editing a page yourself, entirely in your browser

If you would like to make the change yourself, you can do so directly on the
GitHub website. Nothing is installed, and nothing you do goes live
immediately — your change is reviewed first, so there is no risk of breaking
anything.

### Step 1: Create a free GitHub account (once only)

If you do not already have one, go to [github.com](https://github.com) and sign
up. It is free. You only ever have to do this once.

### Step 2: Find the page you want to change

All the documentation lives in the **`docs`** folder of this project. Each help
topic is a single file ending in `.md` (this is just a plain-text format called
Markdown — more on that below).

The easiest way to find a page:

1. Open the help website and go to the page you want to fix.
2. Note its title, then browse to the
   [`docs` folder on GitHub](https://github.com/phinor/adam-docs/tree/main/docs)
   and look for a file with a matching name. For example, the **Quick Start
   Guide** page is `quick-start-guide.md`.

Click on the file to open it.

### Step 3: Start editing

At the top-right of the file you will see a **pencil icon** (✏️). Hovering over
it shows the words *"Edit this file"*. Click it.

> If GitHub shows a message that says *"You need to fork this repository to
> propose changes"*, click the button it offers. A "fork" is just your own
> personal copy — GitHub creates it for you automatically, and you can carry on
> editing straight away.

You are now looking at the text of the page in an editable box. Make your
changes just as you would in any text editor — fix the typo, reword the
sentence, add the missing step.

### Step 4: Describe and propose your change

1. Scroll to the bottom of the page (or click the green **Commit changes…**
   button at the top-right).
2. In the small form that appears, type a short description of what you
   changed, for example *"Fix typo on the enrolment page"* or *"Add missing
   step for archiving a pupil"*.
3. Make sure the option **"Create a new branch for this commit and start a pull
   request"** is selected (GitHub usually selects it for you), then click
   **Propose changes**.
4. On the next screen, click the green **Create pull request** button, and then
   **Create pull request** once more to confirm.

That's it. A **pull request** is simply a polite way of saying *"here is a
change I'd like you to consider."* You have not changed the live site — you
have suggested a change, which someone on the team will review, comment on if
needed, and then approve.

### Step 5: What happens next

Once your change is approved and merged, it goes live on
[help.adam.co.za](https://help.adam.co.za) automatically within a few minutes.
If a reviewer has a question, they will leave a comment on your pull request and
GitHub will email you, so keep an eye on your inbox.

## A few simple writing conventions

To keep every page reading the same way, please try to follow these habits.
They are easy, and a reviewer will happily tidy up anything you miss — so do not
let them stop you from contributing.

- **Write plainly.** Short sentences and everyday words are best. Assume the
  reader is capable but new to the task.
- **Names of buttons, tabs and fields go in bold.** In Markdown you make text
  bold by putting two asterisks on each side, like `**this**`, which appears as
  **this**. For example: *"click on the **Save** button."*
- **Describe menu paths as a sentence** rather than with arrows. For example:
  *"click on the **Administration tab**, then under the **Absentee
  Administration heading**, click on **Edit the absentee reasons**."*
- **Use British/South African spelling** (organise, colour, enrolment) to match
  the rest of the manual and ADAM itself.
- **Headings** start with a `#`. One `#` is the page title, `##` is a section,
  `###` is a sub-section. You rarely need to add these, but if you do, follow
  the pattern already on the page.

If you are unsure how to format something, the safest thing to do is copy the
style of the text already around it.

## Adding or updating a screenshot

Screenshots help enormously, but they need a little care:

- **Never use a real school's data.** Screenshots are always captured against a
  demonstration school, never a live/production site, so that no pupil or family
  information is ever shown.
- Save the image in the folder that matches the page, under
  `docs/assets/screenshots/`. For example, images for the **Roll Calls** page
  live in `docs/assets/screenshots/roll-calls/`.
- If adding a screenshot through the website feels fiddly, it is often easier to
  simply **email the image** to [help@adam.co.za](mailto:help@adam.co.za) and
  tell us where it should go. We will place it for you.

## Questions?

If anything here is unclear, or you get stuck at any step, please email
[help@adam.co.za](mailto:help@adam.co.za). We would much rather help you through
it than have you give up — every correction, however small, makes the manual
better for everyone.
