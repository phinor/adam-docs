# Troubleshooting Email Delivery

It occasionally happens that a recipient will not recieve an email message that has been sent by ADAM. This is most notable when parents, for example, are waiting for a [password reset email](parent-and-pupil-portal.md#forgotten-passwords) that never arrives.

When trying to find a problem, the first thing to note is that ADAM itself is not responsible for delivering mail. It should be configured to talk to your school’s existing mail service and send mail out via that mechanism. Thus, your school’s IT department must be brought into the conversation when this is provided for. Some schools prefer to use a special mail delivery service for mail from ADAM, but these can be costly with large quantities of mail.

The following check list may help to resolve matters:

## 1) Is the email address captured correctly in ADAM?

Parents might have even received emails from ADAM before, but perhaps their email address has been changed and now reflects a different address or an incorrect address. Please check with the recipient that their email address has been captured correctly on ADAM.

One other occurrence is that there might be duplicated profiles that may have different addresses. ADAM may be sending to the incorrect address from a duplicate profile.

### Beware identity fraud!

It may help to verify the parents’ details via a different communication channel other than by email. Sometimes, people will claim that their login doesn’t work, and it appears that they are using the same email address. They might even ask you to copy and paste their email address to replace what you currently have on file.

Please be very careful that you are sure you recognise the address and that you have verified that the request is not from a malicious party trying to get access to that parent’s information.

As an example of how this works: an email address might be “[adam@example.co.za](mailto:adam@example.co.za)”. The parent emails you from “[adam@exampIe.co.za](mailto:adam@exampIe.co.za)” claiming that they are not receiving their email messages. When you copy and paste the second email address over what appears to be the same address, they are happy and can now log in. Why has this worked?

The second email address is shown above using a capital “i” instead of a lower case “L”. While they appear to be the same, ADAM treats “example” and “exampie” as very different addresses. By changing the address, you have potentially given someone else full access to that parent’s details, including the ability to update them.

## 2) Has the email been delivered to their “spam” or “junk” folder?

Please ask the parent to check if the email has not been delivered by mistake to their “spam” or “junk” mail folder. If this is the case, kindly ask the parent to mark the message as “not spam” or “not junk” to reduce the chances of future messages being classified as such. Note that this is not foolproof and some email services have very strict protocols to define what counts as spam mail and what is allowed through to the end-users’ inboxes. We, at ADAM EduTech, have no control over your parents’ email servers and are powerless to make any changes to how their servers are administered.

Advanced users might set up filters on their email which may mistakenly file or route messages sent to the user to other folders and so the message for changing a password might have even been filed away with the school news letters.

### Reducing spam mail detection

If you find that mail sent from ADAM is commonly detected as spam or junk mail, there are some proactive steps that your school’s IT department can take to reduce this from happening. Please see the separate section on how to [mitigate against spam problems](messaging-centre.md#the-messaging-centre-and-email-spam).

## 3) Can the IT department shed any light?

Because ADAM uses your school’s mail infrastructure (or even a third party service of your choosing) to deliver email, if mail is not arriving at its destination, your IT department personnel will be able to check the mail delivery logs and check:

1.  The message was, in fact received.
2.  The message was passed on to the recipient for onwards delivery.
3.  Any errors that might have been generated while communicating with the recipient email server.
