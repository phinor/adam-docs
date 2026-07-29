# Two-Factor Authentication for Administrators

## Introduction

This page covers what an ADAM administrator needs to do about two-factor authentication: the settings that control it, how to see which staff have set it up, and the actions you can take on someone else's account.

Staff who want to set two-factor authentication up on their own account should read [Two-Factor Authentication](two-factor-authentication.md#two-factor-authentication) instead.

## The 2027 requirement

From **1 January 2027**, every staff member who uses ADAM must have two-factor authentication set up. This is not a setting you can decline — on that date ADAM begins asking any staff member who has not set it up to do so before they can continue.

You do not have to wait, and there is a good reason not to. A school that switches the requirement on early moves its staff over gradually, with help available and at a time of its choosing. A school that waits until the deadline moves every staff member on the same morning, which is usually the first morning of a term.

We would suggest, in order: train your staff, encourage them to set it up voluntarily, watch the [coverage screen](#the-coverage-screen) until the number of people left is small, help those people individually, and only then switch the requirement on.

## The settings

Click on the **Administration tab**, then under the **Site Administration** heading click on **Edit site settings**. Choose the **Security** tab and find the **Two-Factor Authentication** heading.

![](assets/screenshots/two-factor-authentication/two-factor-authentication-11.png)

### Requiring two-factor authentication

Set **Two Factor Authentication Forced For Staff** to “Yes” to require it of every staff member now, ahead of the deadline.

Staff with elevated privileges are always required to use two-factor authentication, whatever this setting says.

### Choosing how often ADAM asks for a code

**Two Factor Authentication Method** decides how often a staff member is asked for their six digits. There are three choices, and the setting starts on **Require OTP once per computer**.

**Require OTP at every login** is the most secure and the most tiring. Someone who signs in several times a day types a code every time.

**Require OTP once per computer per day** asks each person once a day on each computer they use. This is the best balance for most schools.

**Require OTP once per computer** asks only when someone signs in from a computer ADAM has not seen them use before. **Remember logged-in machines for**, under the **Login Settings** heading on the same tab, then decides how long that recognition lasts before ADAM asks again.

!!! warning
    Recognition is per person, not per computer, so being remembered on a staffroom desktop does
    not wave anybody else through — each staff member is asked for a code the first time they
    sign in there. What it does mean is that somebody who learns a staff member's password can
    sign in as them from that same shared browser without needing a code, for as long as the
    recognition lasts. On shared computers, prefer **Require OTP once per computer per day**, or
    keep **Remember logged-in machines for** short.

ADAM recognises a computer by a cookie stored in the browser. Clearing cookies, or using a different browser on the same computer, makes it a computer ADAM has not seen before.

Staff can see how many of their own computers are currently remembered, and sign them all out — useful if a laptop is lost. You can do the same on their behalf; see [managing another staff member](#managing-another-staff-member).

### Allowing for clock drift

A one-time PIN is worked out from the time of day, so ADAM's clock and the clock on the staff
member's phone have to agree. **Two Factor Authentication Time Drift** decides how far apart they
are allowed to be, in **seconds**. The choices are 10, 15, 20 and 30, and it starts on 30.

A code only lives for thirty seconds, so the drift cannot usefully be set higher than that. A
smaller number is more secure, because a code someone glimpses over a shoulder stays usable for
less time; a larger number is more forgiving of a phone whose clock is slightly out.

If a lot of staff suddenly cannot enrol or sign in, suspect the server's clock rather than this
setting. A server whose time has drifted affects everybody at once, which is the usual sign.

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

## Managing another staff member

Both actions below appear next to a staff member's name in the **Set up** table on the [coverage screen](#the-coverage-screen).

### Removing someone's two-factor authentication { #removing-two-factor-for-another-staff-member }

Use this when somebody cannot get in and has no recovery codes left. Click **remove 2FA** next to their name.

ADAM asks you to confirm your own password and your own six-digit code first, unless you have confirmed recently — a second removal soon after the first is not challenged. This is deliberate: the list in front of you is every staff member at the school, and a stranger sitting at an unattended administrator's desk should not be able to work down it.

Once you confirm, ADAM returns you to the coverage screen. It does not remove the staff member's two-factor authentication for you — click **remove 2FA** again to finish the job.

!!! warning
    Removing two-factor authentication does not remove anything from the staff member's phone. When they set it up again they must scan a new QR code, and they should delete the old entry from their authenticator app first — the old entry's codes will never work again.

If your school requires two-factor authentication, the staff member is asked to set it up again the moment they next sign in.

### Signing out their remembered devices

Use this when a staff member's laptop or phone has been lost or stolen and you want every computer ADAM was trusting for them to be forgotten straight away. Click **sign out devices** next to their name.

Every remembered computer is forgotten, and the next sign-in from each asks for a code. Their second factor itself is untouched, and so are their recovery codes.

ADAM emails the staff member to tell them this happened, so that they are not left wondering why they are suddenly being asked for a code again. If there was nothing to sign out, no email is sent.
