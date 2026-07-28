# Two-Factor Authentication

## Introduction

The data stored in the ADAM database is very sensitive data. To help protect this data, ADAM allows you to protect your account with Two-Factor Authentication (2FA).

Two-factor authentication is used by many banks to ensure that your transactions are genuine: when you initiate a payment or transaction, you are asked to type in a a “one-time-PIN” (OTP) or approve the transaction from your phone. The OTP, or the approval from your phone, is known as the “second factor” in the authentication process.

An account protected with Two-Factor Authentication will not allow a login without the one-time-PIN.

ADAM’s two-factor authentication system works using an Authenticator App that must be installed onto your phone. The Authenticator App will generate the One Time PIN. It is not sent by SMS and it is not linked to any specific phone number. After it has been set up, the app will not require any airtime or data to use.

!!! warning
    From **1 January 2027**, two-factor authentication is required for every staff member who uses ADAM. You do not need to wait for that date — you can set it up now, and we would encourage you to. Once the requirement takes effect, ADAM will ask you to set it up the next time you sign in, and you will not be able to use ADAM until you have.

Two-factor authentication is already required for accounts with elevated privileges, whatever your school has chosen.

## Supported Authenticator Apps

There are many different Authentor Apps that you can use. Popular ones include **Google Authenticator** (by Google LLC), **Microsoft Authenticator** (by Microsoft Corporation), or **Twilio Authy Authenticator** (previously simply “Authy”, by Twilio).

![](assets/screenshots/two-factor-authentication/two-factor-authentication-01.png)

Google Authenticator

![](assets/screenshots/two-factor-authentication/two-factor-authentication-02.png)

Microsoft Authenticator

![](assets/screenshots/two-factor-authentication/two-factor-authentication-03.png)

Twilio Authy Authenticator

All of these apps are available for download from your preferred app store.

If your school makes use of Google Workspace, we recommend using the Google Authenticator. If your school makes use of Microsoft 365, we recommend using Microsoft Authenticator.

## Adding Two-Factor Authentication to your account

First, [download and install an authenticator app](#supported-authenticator-apps) from your app store.

You can reach the setup page in two ways. If ADAM is waiting for you to set two-factor authentication up, it takes you there itself the next time you sign in. Otherwise, sign in as normal, click on the **Staff tab**, and then under the **Security Administration** heading click on **Manage your Two-Factor Authentication**.

The setup page asks you to do two things, in order.

### Step 1: Scan this code

ADAM shows a QR code alongside a written **Two-Factor Authentication Secret**. Scanning the code is simply a shortcut that saves you typing the secret into your phone by hand — the two carry the same information.

![](assets/screenshots/two-factor-authentication/two-factor-authentication-04.png)

!!! note
    The QR code in the picture above has been deliberately corrupted so that it cannot be scanned. Scan the code on **your own screen** — every account's code is different.

Open the authenticator app you installed, and choose its option to add a new account. The app will ask permission to use your camera so that it can scan the code. In the Google Authenticator app, for example, this is the **+** button at the bottom right of the screen.

![](assets/screenshots/two-factor-authentication/two-factor-authentication-05.png)

*An example of three accounts that have been set up for Two-Factor Authentication and how they appear in the Google Authenticator App. If you use a different App, it will look different!*

Once the code has been scanned, the app lists the account and shows a six-digit number beneath it. That number changes every thirty seconds.

### Step 2: Enter the six digits

The last step tells ADAM that your app really did save the secret. Type the six digits currently shown in your app into the **Confirmation Code** box, and click on **Add Two-Factor Authentication Protection**.

![](assets/screenshots/two-factor-authentication/two-factor-authentication-06.png)

If the digits were correct, ADAM confirms that two-factor authentication is now protecting your account, and shows you your recovery codes. **Do not leave that page without saving them** — see [Recovery codes](#recovery-codes) below.

![](assets/screenshots/two-factor-authentication/two-factor-authentication-07.png)

If ADAM says the code was wrong, the most likely reason is that the six digits changed while you were typing. Try again with the number now showing in your app. If it fails repeatedly, see the [frequently asked questions](#frequently-asked-questions) below.

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

## Remembered devices

Depending on how your school has set ADAM up, it may not ask for your six-digit code every single time you sign in. It can instead remember the computer you are using, and skip the prompt for a while. Your school's administrator chooses this — see [how often ADAM asks for a code](two-factor-authentication-for-administrators.md#choosing-how-often-adam-asks-for-a-code).

Where that is in use, your two-factor authentication page shows a **Remembered devices** card telling you how many computers are currently trusted to skip the prompt.

!!! tip
    If you have signed in on a computer that is not yours — a shared office machine, a hotel, a friend's laptop — or if a laptop has been lost or stolen, use **Sign out all devices**. Every remembered computer is forgotten, and the next person to sign in on any of them has to enter a code.

Signing devices out does not remove two-factor authentication from your account and does not affect your recovery codes. It only means the code prompt comes back.

You may also see this card show nothing to sign out. That simply means no computer is currently being trusted — either because none has been, or because your school asks for a code at every sign-in.

## Removing Two-Factor Authentication

Once you have added two-factor authentication, you can remove 2FA by clicking on the **Staff tab**, and then under the **Security Administration** heading clicking on **Manage your Two-Factor Authentication**. If it is enabled on your account, you will see the following:

![](assets/screenshots/two-factor-authentication/two-factor-authentication-08.png)

Click on the **Remove Two-Factor Authentication** option at the bottom to begin the process. ADAM opens a page headed **Remove two-factor authentication**.

You must then enter your ADAM password to confirm that you’d like to remove Two-Factor Authentication from your account:

![](assets/screenshots/two-factor-authentication/two-factor-authentication-09.png)

Once removed, ADAM will show the options to re-enrol your account in the Two-Factor Authentication setup, including a new QR code. If you see the QR code, then your account is no longer protected by Two-Factor Authentication.

Please note that if your account requires Two-Factor Authentication, if you remove it, you will be forced to re-add two factor authentication immediately and will not be able to use ADAM until this is done.

## Frequently Asked Questions

### ADAM is not sending me the OTP. How do I log in?

ADAM does not send the One-Time PIN (OTP) - it is generated by the Authenticator App on your phone. You need to open the Authenticator App and get the OTP from within the App.

The OTP is generated by the App. It does not use any data and does not require you to have any airtime on your phone, and you don’t need any cell reception.

### How do I log in if I don’t have my phone with me?

The short answer is that you can’t!

Your ADAM administrator will be able to [remove two-factor authentication from your account](#removing-two-factor-authentication-for-another-staff-member). You will then be able to log in normally without having to provide a one-time-PIN.

Again, note that if you choose to re-enable two-factor authentication on your account, you will need to scan a new QR code which will generate different OTPs to your old scan.

If you are the ADAM administrator from your school and you lose your phone and are therefore unable to login to ADAM, you will need to contact us for support. We will then need to perform a manual verification process to ensure that your request is genuine.

### I have a new phone or don’t have the App installed anymore. How do I log in?

The short answer is that you can’t.

See above for how to have Two Factor Authentication removed from your account to allow a log in.

### I removed the app because I don’t want to use two factor authentication any more. Now I can’t log in.

Please be aware that the only time that ADAM and your Authenticator App will communicate is when the QR code is first scanned. After that, there is no synchronisation or communication of any kind between ADAM and the Two-Factor Authentication app that is installed on your phone.

!!! warning
    If you remove the app from your phone, or remove the ADAM OTP from within the app, it does not remove Two-Factor Authentication protection from your account. If you remove the code from your app before you remove two-factor authentication from your account, you will no longer be able to log in.

Similarly, if you remove the protection from your account, it does not automatically remove the code from your app.

If you lose your phone or are unable to generate an OTP for whatever reason (perhaps your battery is flat), only your [ADAM administrator can remove the 2FA protection](#removing-two-factor-authentication-for-another-staff-member) from your account.

### I have two ADAM logins and need to scan two different QR codes for the two different accounts. Can I do this?

Yes, most authenticator apps will support multiple accounts. Please be aware that if you scan a second QR Code for the same ADAM server, the Authenticator App *may* ask you if you want to replace the OTP.

Most authenticator apps will also allow you to rename the OTP entry so that you can differentiate between the two entries in your phone.

### The Authenticator App shows me two OTPs. Which one do I use?

If you remove and re-add Two-Factor Authentication, you will have to scan a new QR Code. Sometimes this means that your Authenticator App will have two entries. Each time ADAM generates a new QR code, it comes with a different secret code which means that every QR code will provide different OTPs.

You cannot use the OTPs generated by an old entry. Please make sure that you remove any old entries that are no longer applicable to avoid confusion!

Sometimes it can be easier to have your ADAM administrator remove your Two-Factor Authentication and then sign up from scratch. Once two factor authentication has been removed from your account, please remember to remove all OTP entries in your Authenticator App before scanning the new QR code.

### I can’t enrol in 2FA because my confirmation code is wrong.

This is very rare, but it can happen. Please make sure that your phone time is accurate.

If this issue suddenly affects lots of users, and if your server is hosted on your network at school, it could also be an issue with the server’s time synchronisation and your network administrator may have to investigate further.

OTPs are generated according to the time of day. The ADAM server knows the current time, your phone knows the current time, and so at any specific time, ADAM can check if the code is the correct one that should be generated by the app.

Most phones will set their time automatically from external sources - often from the network provider. In general these times are accurate to within a few seconds of universal time. However, some phones have been seen to NOT update their time and run a minute or more out of sync with universal time.

If this happens, there will be a mismatch between the codes that your phone generates and the code that the server is expecting.

## Setting up your ADAM server for Two-Factor Authentication

2FA is ready to be used by any individual staff member and no additional setup is required. However, it is possible to force that 2FA is used by all staff and some other settings that control how often the OTP is requested.

### Two-Factor Authentication Settings

Within the Site Settings, navigate to **Security** tab and scroll down to the **Login Settings** heading.

The relevant settings are highlighted below:

![](assets/screenshots/two-factor-authentication/two-factor-authentication-11.png)

### 2FA Authentication Windows

The **Two-Factor Authentication Window** determines how many OTPs should be allowed on either side of the window. Because OTPs are time-based, discrepancies in the user’s cellphone time and server time can play a factor.

In most scenarios, these two clocks should be independently set (phones by GPS, servers by network time servers (NTP)) and should be very close to one another. This might not always be possible. To increase the life-span of an OTP, increase the window.

Each window represents 30 seconds. The default setting is 2 and will cause the server to check OTPs 2 windows ahead and 2 windows behind its current time to allow for time discrepancies. This can be increased to 3 (not advised) which effectively increases the lifespan of any OTP to 3 minutes - 1,5 minutes behind and 1,5 minutes ahead of the server’s current time.

1 is the most secure setting and 3 is the least secure setting. This is because smaller windows mean it is harder to “steal” and later use an OTP because it is valid for a shorter period of time.

### Forced Use of 2FA

Administrators can force all staff members to make use of Two-Factor Authentication by changing a setting the [Site Settings](changing-site-settings.md#changing-site-settings). Within the Site Settings, navigate to **Security** tab and scroll down to the **Login Settings** heading.

Change the setting **Two-Factor Authentication Forced For Staff** to “Yes”.

When implementing 2FA across your entire staff body, we encourage a phased in approach before implementing this setting. Please be sure to conduct training with your staff that use ADAM and get as many of them as possible to use the feature to [voluntarily enrol](#adding-two-factor-authentication-to-your-account) for two-factor authentication before it becomes a mandatory requirement.

### Changing How Frequently is the OTP required

The **Two-Factor Authentication Method** determines when users will be requested for their OTP. The default option is at every login, but this can be frustrating to users who make use of ADAM throughout the day. Other options are to remember it once per computer or once per computer per day.

#### Require OTP at every login

If this is set, your staff members will have to enter their OTP each time they log into ADAM. This is very secure, but can also be frustrating for your staff, especially for those that use it many times per day.

#### Require OTP once per computer per day

ADAM will ask the users once each day on each device that the user logs in with for their OTP. This is the best balance between security and usability without frustrating users too much.

#### Require OTP once per computer

Whenever ADAM detects that a user is using a new computer, it will ask them for an OTP. If they are using a computer that they’ve used in the past, ADAM won’t ask them for an OTP. This is normally fine for users who have dedicated computers that they alone use. Note that ADAM may still ask for an OTP from time-to-time, but it may be as infrequently as once per month.

If the “once per computer” option is chosen, then ADAM will ask for the OTP each time the user logs in on a new computer. Have a look at the **Remember logged-in machines for** setting. This means that ADAM will forget about a computer after a certain number of days and will automatically re-ask for the OTP when it does.

ADAM uses a cookie stored on the devices to remember its identity. If the cookies are cleared, ADAM will effectively see the computer as a new device and ask the user for their OTP. Cookies are also specific to user sessions, browsers and more. Switching to a different web-browser on the same computer will also count as a new device and will require a new OTP.

## Removing Two Factor Authentication for another staff member

If a user is enrolled for Two Factor Authentication, they can remove 2FA authentication by navigating to **Administration → Security Administration → Manage Two Factor Authentication** and then clicking on the **Remove 2FA** option next to their name in the list.

!!! warning
    Note that if 2FA is reinstated by a user after being removed, their app will have to be updated with a new QR Code. ADAM does not allow a previous code to be used. The code should be removed from the 2FA app when 2FA is disabled from the account.

## Troubleshooting 2FA and OTPs

The most common issues arise from the fact that the OTP is time-based.

If, for example, there is a delay in entering the OTP, the OTP may expire. Although the OTP changes every 30 seconds, ADAM will allow an OTP to be used for a short while after it disappears from the app. This is to help offset the any potential differences in clocks between the phone and the server.

Because the OTPs are time-based, it is important that the server and the phone both have accurate time of day set. Most phones have their time set via their GPS chips and so are normally accurate within a second. Servers should be synchronised to an internet time server and be configured with the correct timezone and are similarly normally accurate within a second.
