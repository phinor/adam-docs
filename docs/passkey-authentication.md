# Passkey Authentication {#h-68qerlruak0n}

## Introduction {#h-6osmass1sayc}

A **passkey** is a safer, easier replacement for your password. Instead of typing in your username and password, you unlock ADAM using the same fingerprint, face recognition, or screen lock that you already use to unlock your phone, tablet, or computer.

Passkeys are stronger than passwords for two reasons:

-   There is nothing to remember, so there is nothing to forget.
-   There is nothing to type, so there is nothing to be phished, guessed, or stolen. A passkey never leaves your device.

ADAM supports passkeys for **staff**, **parents**, and **pupils**. You can continue to use your password as normal - a passkey is an extra way of logging in, not a replacement.

On the ADAM login page you will see a **Log in with a passkey** option. Clicking it will ask your device to confirm it is you (usually by fingerprint or face) and then log you in.

## What you need {#h-lxf32t1p38m}

To use a passkey, you need one of the following:

-   A **modern phone or tablet** with fingerprint or face unlock (for example, an iPhone with Face ID or Touch ID, or an Android phone with a fingerprint sensor).
-   A **modern laptop or desktop** with a fingerprint reader, Windows Hello, or Mac Touch ID.
-   A **hardware security key** (such as a YubiKey).

Any reasonably up-to-date device will work. You do not need to install any extra app. Passkeys are a standard feature built into iOS, Android, Windows, macOS, and all modern web browsers.

## Setting up a passkey {#h-v1fwy1zdkfnn}

You can add as many passkeys to your ADAM account as you like - typically one for each device you use (for example, one on your phone and one on your work laptop).

### If you are a staff member {#h-55p216g78o9y}

Staff who have not yet enrolled a passkey will see a card titled “Log in with your fingerprint or face” on their dashboard, with a **Set up a passkey button**. Clicking it opens the Passkeys management page. From there, click **Register a new passkey**, and confirm with the device’s fingerprint, face scan or PIN. The new passkey is then listed on the management page.

To register additional pass keys you can:

1.  Log in to ADAM as normal, using your username and password.
2.  Click the **Set up a passkey** link that appears on your dashboard. If you do not see that link, go to **Staff → Security Administration → Manage Passkeys**.
3.  Click **Register a new passkey**.
4.  Your device will prompt you to confirm - for example, by using your fingerprint, face, or PIN.
5.  You can click on the **rename** option to give your passkey a descriptive name (for example, "My iPhone" or "Work laptop") so that you can recognise it later.

### If you are a parent or pupil {#h-jqwd0zavk7lv}

1.  Log in to the parent or pupil portal with your username and password.
2.  Click the **Set up a passkey** link on the portal page. If you do not see it, open the portal menu and choose **Manage your passkeys**.
3.  Click **Add a passkey**.
4.  Your device will prompt you to confirm using your fingerprint, face, or PIN.
5.  Give your passkey a name.

That's it. Next time you visit the login page, you can skip typing your password.

## Logging in with a passkey {#h-wnakepceqinj}

1.  Open the ADAM login page on a device where you have set up a passkey.
2.  Click the **Log in with a passkey** button.
3.  Your device will ask you to confirm with your fingerprint, face, PIN, or screen lock.
4.  You will be logged in.

There is no username or password to type in. On a phone, the whole process usually takes a few seconds.

## Managing your passkeys {#h-aep8uv6201tz}

You can view, rename, and remove your passkeys at any time from the **Manage Passkeys** page. Each passkey is shown with the name you gave it, the device type it was created on, and the date it was last used.

-   **Rename** a passkey if you change the device it is on or want a clearer label.
-   **Remove** a passkey that is no longer needed - for example, if you have sold or lost the phone it was on, or left a workstation.

Removing a passkey from ADAM does not remove it from your device, and removing it from your device (for example, by resetting your phone) does not remove it from ADAM. If you replace a device, it is a good idea to both add a new passkey for the new device and remove the old passkey from ADAM.

## Frequently Asked Questions {#h-e6j6fs45pp82}

### Does the school or ADAM see my fingerprint or face? {#h-81nitqqzj3cs}

No. Your fingerprint and face recognition data never leave your device. Your phone or laptop simply tells ADAM "yes, this is the right person" - it does not send any biometric information. ADAM never sees, stores, or has access to your fingerprint or face.

### What happens if I lose my phone? {#h-12hpm6pj7vkw}

Your account is still protected, because the passkey is locked behind the phone's screen lock. A person who finds your phone cannot use the passkey without your fingerprint, face, or PIN.

If you had a passkey only on the lost phone, log in on another device using your username and password, open **Manage Passkeys**, and remove the entry for the lost device. Then add a new passkey on your replacement device.

If you cannot log in at all because your only login method is a passkey on the lost phone, ask your ADAM administrator to remove your passkey so that you can log in with your password.

### Can I have more than one passkey? {#h-422xvv7apkol}

Yes. We recommend adding a passkey on each device you use to access ADAM. If one device is lost or replaced, the others continue to work.

### How is a passkey different from Two-Factor Authentication? {#h-vfxwlinqs1ci}

Two-Factor Authentication adds a one-time code on top of your password. A passkey replaces the password with something stronger.

Passkeys are generally considered more secure than a password with 2FA, because there is no shared secret that can be phished or intercepted. The passkey itself can only be unlocked on your device, by you.

### Can I use a passkey on a shared or public computer? {#h-xxsvpuqjxta8}

It is usually better not to. Paslogskeys are tied to a device, so adding a passkey on a shared computer means anyone who can unlock that computer can also log in to your ADAM account.

Use a passkey on devices that only you use. For shared or public computers, log in with your username and password as normal.

### I got a new phone. How do I move my passkey? {#h-rem1rsgdjgd1}

If your new phone is set up with the same cloud account (Apple ID, Google account, or Microsoft account) as your old phone, your passkeys may move across automatically. This depends on your cloud account settings.

The simplest approach is to treat the new phone as a new device: log in to ADAM with your username and password, add a fresh passkey for the new phone, and then remove the old passkey from the **Manage Passkeys** page.

### The browser is not offering to save a passkey. {#h-ffs6a5l28l1h}

Very old browsers, or browsers in private or incognito mode, may not support passkeys. Check that you are using an up-to-date browser (Chrome, Edge, Safari, or Firefox), and that you are not in private browsing mode.

On a desktop computer without a fingerprint reader, the browser may offer to use your phone instead - it will show a QR code that you scan with your phone. Your phone's fingerprint or face unlock is then used to confirm the login.

## For Administrators {#h-jx35t0j2mdn9}

No server-side setup is required to enable passkeys. Passkey login is available to all users out of the box.

ADAM Super-Administrators can view and revoke any staff member’s passkeys via the **Manage Staff Passkeys** page. The page lists only those staff who have at least one passkey enrolled. Selecting a staff member shows their passkeys with the date each was enrolled and last used; clicking remove revokes the passkey immediately.

Removing a passkey does not prevent the staff member from continuing to log in with their password.
