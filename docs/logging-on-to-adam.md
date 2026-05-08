# Logging on to ADAM {#h-clv8x8a7ujwh}

## Passkeys {#h-9zn9jl9lfze1}

A passkey is a credential stored on the user’s device (phone, tablet or computer) that signs the user in to ADAM using a fingerprint, face recognition or device PIN, instead of a password. Passkeys are resistant to phishing, are not reusable across sites, and never travel across the internet, so they are considerably safer than passwords. ADAM supports passkeys for staff, parents and pupils.

Each user may enrol more than one passkey — for example, one on their phone and one on their work laptop — and each passkey can be named so that it is easy to identify later. Passkeys never replace a user’s password and Two-Factor Authentication settings: they are an additional, optional way to log in, and the password and one-time PIN remain available as a fallback.

For a more detailed walkthrough, see the dedicated [Passkey Authentication](passkey-authentication.md#h-68qerlruak0n) page.

### Signing in with a Passkey {#h-b08u2kb04cq8}

On the staff, parent and pupil log-in pages, ADAM offers a Log in with a passkey button (marked with a fingerprint icon) above the username and password form. The button is only shown if the browser supports passkeys; older browsers will continue to see the password form on its own.

To sign in:

1.  Open the appropriate ADAM log-in page.
2.  Click Log in with a passkey.
3.  The browser will prompt for the device’s biometric (fingerprint or face) or PIN.
4.  Once the gesture is recognised, ADAM signs the user in and takes them to their dashboard or portal home.

A successful passkey login satisfies the Two-Factor Authentication requirement on its own — the user is not asked for a one-time PIN as well. See [Passkeys and Two-Factor Authentication](#h-p9xu2wahh50k) below.

### Setting Up a Passkey for Staff {#h-la12kjftrq15}

The first time a staff member logs in after passkeys are enabled, their dashboard will display a card titled “Log in with your fingerprint or face”, with a Set up a passkey button. Clicking the button takes the staff member to the Passkeys management page.

Once a passkey has been registered, the dashboard card disappears. To return to the Passkeys management page after that, see [Managing Your Passkeys](#h-tr6n82c0msvb) below.

To register a new passkey:

1.  On the Passkeys page, click Register a new passkey.
2.  Enter a name for the passkey when prompted (for example, “My iPhone” or “Office laptop”). The name is only used to identify the passkey on this management page.
3.  The browser will ask the operating system to create a passkey. On a phone or tablet this typically requires a fingerprint or face scan; on a desktop it may use Windows Hello, Touch ID, a security key, or a paired phone.
4.  Once the device confirms the gesture, the passkey is saved and listed on the management page.

### Setting Up a Passkey for Parents and Pupils {#h-x5pxak7fa2ic}

Parents and pupils manage their passkeys through the portal:

-   Family Portal → Security → Manage your passkeys
-   Pupil Portal → Security → Manage your passkeys

The Pupil Portal menu item is only shown to pupils whose accounts have logins enabled (see [Enabling and Disabling Pupil Logins](#h-pgvqow2v6moj)).

Until the user has registered their first passkey, the top of the portal page will also show a “Log in with your fingerprint or face” card with a Set up a passkey button, which is a shortcut to the same page. The registration steps are the same as those described under [Setting Up a Passkey for Staff](#h-la12kjftrq15).

### Managing Your Passkeys {#h-tr6n82c0msvb}

The Passkeys management page lists every passkey enrolled on the current account, showing the name, the date it was enrolled, and the date it was last used. Each passkey has two actions:

-   rename — change the name shown for the passkey (up to 100 characters). This does not affect the credential itself.
-   remove — permanently delete the passkey from ADAM. The user will no longer be able to sign in with that passkey, although the credential will still take up space in the device’s passkey manager (and can be removed there separately).

Users should remove a passkey if the device it lives on has been lost, sold, or is no longer in their possession. As long as the user can still log in another way (using their password and Two-Factor Authentication, or another passkey on a different device), they can remove a stale passkey themselves. Should a user lose their only passkey and be unable to log in to delete it, an administrator can remove it on their behalf — see [Revoking a Staff Member’s Passkey](#h-83ojpg1gzptn).

### Revoking a Staff Member’s Passkey {#h-83ojpg1gzptn}

If a staff member loses a device, has it stolen, or leaves the school, an ADAM Super-Administrator can revoke any of their passkeys without needing the staff member’s cooperation. This is reached through the Manage Staff Passkeys page, where a Super-Administrator can:

1.  Select the staff member from a drop-down list of staff who have at least one passkey enrolled.
2.  Review the passkeys on that staff member’s account, with the name, date enrolled, and date last used for each.
3.  Click remove against any passkey that should be revoked.

The Super-Administrator cannot rename a staff member’s passkey or register a new passkey on their behalf — only the staff member, signed in as themselves, can do that. The same is true of parent and pupil passkeys: there is no administrator override for these, because they are tied to a specific device that only the parent or pupil has access to. If a parent or pupil cannot remove their own passkey, they should reset their password and use that to sign back in, then delete the passkey from their management page.

### Passkeys and Two-Factor Authentication {#h-p9xu2wahh50k}

A passkey is itself a strong second factor (the device the passkey is stored on, plus the biometric or PIN that unlocks it), so when a user logs in with a passkey ADAM does not additionally prompt for a one-time PIN. This is true even when the Two Factor Authentication Forced for Staff setting (see [Login Settings](#h-76mtqpklmjiq)) is enabled.

Users who log in with their username and password continue to be prompted for a one-time PIN exactly as before. The Two-Factor Authentication setting therefore continues to govern password-based logins, and is unaffected by passkey enrolment.

### Browser and Device Requirements {#h-y88o4miqy8a3}

Passkeys require a modern browser (recent versions of Chrome, Edge, Firefox or Safari) and a device with a fingerprint reader, face camera,pass or device PIN. ADAM must be reached over an HTTPS connection — passkeys will not work on plain HTTP. Users on older browsers, or on devices without an authenticator, will not see the Log in with a passkey button and should continue to use their password.

### Audit Trail for Passkeys {#h-ozo7ognfmjip}

Every passkey enrolment, rename, removal and login is recorded in the ADAM logs alongside other authentication events. Each passkey’s “Last used” date on the management page is also updated on every successful login, so users and administrators can see at a glance which credentials are still in active use.

## General Login Settings {#h-jcwooevtgo7g}

A number of common login settings can be found in the [Site Settings](changing-site-settings.md#h-3j2qqm3). Navigate to the “Security” tab.

### Active Directory Authentication {#h-xde759ytj24y}

If your school has an Active Directory server, you can capture its details here. The LDAP module may need to be installed before this will work.

If ADAM will communicate via the public internet with your AD server, you must use a Secure LDAP Connection to prevent your users’ login credentials from being visible.

### OAuth Authentication Settings {#h-ijzca4x95vyk}

This can allow your users to authenticate to ADAM if they are signed in with their school-issued Google or Microsoft account. ***Please contact*** ***[help@adam.co.za](mailto:help@adam.co.za)*** ***before you enable any of these settings.***

### Internal Password Administration {#h-ecvmyawii5uh}

Here you can set the minimum password length required. Note that passwords shorter than 8 characters are not permitted.

The “Allow External Authentication Failover” feature allows users who would normally log into ADAM by authenticating against their Active Directory Server to still log in, even if their Active Directory Server is not available. Note the following:

The failover service works by storing an AD-validated encrypted hash of the user’s password as if it were an internally managed password. On future login attempts if the AD server is not available, ADAM will check the supplied password against the stored hash.

This is no less safe than having ADAM manage user passwords itself. On a successful login, ADAM will verify the users password against the hash stored in the database and, if necessary, update the password with a new hash.

-   This is not password *synchronisation*, rather password *caching*. ADAM can only remember passwords it has seen itself and which the AD server has verified as being correct. ADAM cannot “fetch” passwords from AD.

-   Users who have never logged into ADAM before will not be able to login during an AD outage for the first time.
-   Users who logged into ADAM a log time ago and who have subsequently changed their password will still have their old passwords cached on ADAM and thus may need to use an old password to get into ADAM if logging in during an AD outage.
-   Take note here of “remember me” type logins which do not require a user to enter their password. Should a user need to login with a password, they may find that they have to enter their previous password which might have changed some time ago.

-   If Active Directory blocks a user’s login attempt for any reason (e.g. account disabled, incorrect password used), ADAM erases the password hash stored.

-   This prevents the user from being able to log in later when the AD server is unreachable and is therefore unable to deny the login.
-   Such a user will not be able to login until the connection to AD is restored.

-   While ADAM is not able to communication with the AD server, user accounts that may be disabled on AD but which have not attempted a login on ADAM since they were disabled, will still be allowed to log into ADAM during an outage.

-   It is important that user accounts in ADAM are also suspended and that AD is not relied upon.

### LDAP Authentication {#h-3e8y3i10wwjb}

In Linux based networks it is possible to have ADAM use a pure LDAP server for authentication. Note that while the Active Directory logins are conducted over LDAP, many of the settings for the AD LDAP implementation have been preconfigured.

### Login Settings {#h-76mtqpklmjiq}

The **Login time out** is the amount of time in minutes that must elapse between any two page loads on ADAM before the user account is considered logged out. Note that typing a message (especially in the [Messaging Centre](messaging-centre.md#h-o6jbiu0gh9e)) is not considered activity because there is no information going between the server and the client computer.

The setting for **Remember logged-in machines** will set a long-term cookie on a computer which ADAM will then use to determine whether a user has logged in from that machine or not. If no user logs in on that machine within that length of time, ADAM will “forget” the machine and the user will consider to be logged in from a new machine. This has implications for Two-Factor Authentication settings (see below!)

Some schools may chose to **Allow “Remember Me” Logins**. This will prevent the login time-out from affecting the user. Schools should be cautioned against allowing this if the computers that staff use are often left unsupervised and unlocked (consider a desktop computer in a classroom which may have pupils in unsupervised, as opposed to a laptop which is more likely to be turned off and locked). The number of days that ADAM can remember a user for can be set with the **Remember Me Duration** setting.

The **Two Factor Authentication Window** allows users a more gracious sliding window with which to use their one-time PINs. Each window is 30s and is defined by the current time of day as determined by the server. OTPs require the time windows to align on the server and client devices. This can cause issues where users are using devices that may not be synchronised accurately to network time, or, indeed, the server is not accurately synchronized.

When the setting is set to 1, for example, ADAM will check both the current window as well as the 1 window before and 1 window after to check if the OTP supplied would be valid in any of them. This allows for approximately 30 seconds leeway in terms of time slippage. A window setting of 3 would allow 90 seconds of time slippage.

Where device and server times are accurate, a setting more than 2 is discouraged.

ADAM can enforce a number of different **Two Facor Authentication Method** policies. Administrators can require OTPs from users at each login, once per computer per day or, the most lenient, once per computer. Where staff make use of shared computers without unique user accounts, the “once per computer” option is strongly discouraged.

Finally, ADAM can ensure that all staff make use of Two Factor Authentication by setting the **Two Factor Authentication Forced for Staff** setting to “Yes”. When staff login for the first time not having previously set up their two factor authentication, ADAM will prompt them to do so and not permit them to proceed with their logins until they have correctly setup their authentication app to generate one time PINs.

### POP3 Authentication {#h-j9g4lz3w9lwa}

ADAM can use a POP3 server as an external authentication source. Provide the necessary settings here to communicate with your POP3 server. This method is not commonly used because generally schools will have another more commonly used authentication source available to them.

## Staff Logins {#h-37g965a9fxch}

Staff logins are governed by a number of different settings in ADAM.

### Site Settings {#h-6vhh2g12hnrg}

Within the [Site Settings](changing-site-settings.md#h-3j2qqm3), navigate to the “Security” tab. Here, a number of settings will affect staff logins.

## Pupil Logins {#h-7qtfqmqt5stl}

ADAM Administrators may also want to see [Understanding Pupil Login](parent-and-pupil-portal.md#h-g3b7qwfm794s).

### Enabling and Disabling Pupil Logins {#h-pgvqow2v6moj}

Pupil logins can be disabled from within the [Site Settings](changing-site-settings.md#h-3j2qqm3). On the Security tab under the heading “Pupil and Family Login”, change the setting “Allow pupil logins” to “No”.

### Default Settings {#h-rtk1k7vbdz1f}

Within the [Site Settings](changing-site-settings.md#h-3j2qqm3), navigate to the “Security” tab. Under the heading “Pupil and Family Login”, ADAM has two settings which dictate the default login options for pupils.

The “Default Login Method” and “Default pupil & family login privileges” settings are automatically applied to any pupils when they are first added to the database. Note that changing these settings will not change any pupils’ login details: they are only used at the moment that the pupil is added to the database for the first time.

## Parent Logins {#h-ic3j5wvtebz7}

Parents may wish to refer to the section on [Logging on to ADAM: A Guide for Parents](logging-on-to-adam-a-guide-for-parents.md#h-3wf37gt5yaio).

ADAM Administrators may also want to see [Understanding Parent Logins](parent-and-pupil-portal.md#h-j9oqjiq3ubit).

Parent logins can be disabled from within the [Site Settings](changing-site-settings.md#h-3j2qqm3). On the Security tab under the heading “Pupil and Family Login”, change the setting “Allow family logins” to “No”.

## Troubleshooting Logins {#h-z8yv3tysouka}

### Parent requests a password reset, but does not receive an email {#h-98p3ofgkmqfm}

There are several possibilities as to why this might happen. If a parent doesn’t receive the password reset email, check each of these possibilities in the following order:

1.  **Check that their email address is captured accurately.** If the incorrect email address is captured, any password reset requests will be sent to the wrong address. In the worst case, this could mean that someone else will get access to their ADAM profile. In some instances, where ADAM can see obvious issues with the email address which makes it invalid (e.g. spaces in the domain), then ADAM won’t even attempt to send the email.
2.  **Check that their ID number is captured accurately.** It may be that ADAM simply isn’t able to match the ID number against any family member. This happens often with passport numbers which change from time to time when a new passport is issued.
3.  **Check that the ID number is linked to only one family profile.** Sometimes divorced or separated parents end up with multiple profiles on ADAM. In these instances, ADAM is unable to determine which family profile is logging in or, by extension, which children it should be showing. You can check if the ID number is associated with the family by searching for it: **Families → Messaging and Communications → Search for ID numbers**. Make sure that only one family profile is shown. If you are searching for a staff member who is also a parent, you should expect to see one family profile and one staff profile appear in the search results. It is only a problem if they have more than one family profile.
4.  **Ask the parent to check that the email hasn’t been delivered to a spam or junk mail folder.** In many instances, emails requesting password changes are treated suspiciously by many email providers and have a higher chance of being flagged as spam.
5.  **Ask your IT department to trace the email’s delivery in your email service’s logs.** It will be helpful to report the time when the parent requested the login. The more accurate the time is, the easier it will be to trace. They should see a record of the message being received from ADAM and it then being delivered onward on to the family member’s email service. If the email server had problems with onward delivery, they should be able to report these to you. The resolution of any problems here will, of course, depend on the issue that your IT department discovers. If, however, there is no record of any email being sent, and assuming that ADAM can send other email without issue, the problem is almost definitely going to be linked to one of the first three points above.

![](assets/screenshots/logging-on-to-adam/logging-on-to-adam-01.png)*Parents tell us that they find the error messages about logging into ADAM* *to be* *unhelpful and vauge. They* *ask* *us to change these messages to show* *more detail about what is wrong**.* *We agree this would help solve problems faster.*

*However, if we do this, it would also help hackers and* *criminals* *find real ID numbers in our system.* *Not only is it against the law to share information with people who shouldn't have it, but it's even more serious because it could put children in danger if someone finds out they go to a certain school.*

### The login is very slow {#h-r7c710tjb2zq}

The most likely reason is that ADAM is implementing a login delay which is based on a sudden influx of failed logins.

If ADAM detects a large number of failed login attempts, it begins to implement a delay before it validates the login. This is done to delay anyone who may be trying to try lots of different passwords in very quick succession using automated tools. This technique, credential stuffing, commonly employed by hackers.

This login delay will resolve over time, assuming that the failed login attempts stop.

ADAM administrators should check the logs for information related to these possible login failures.

A second reason, specifically for schools who use remote authentication mechanisms is that the communication between the ADAM server and the authentication server is being delayed. This could be because of network congestion or a performance issue with the authentication server.
