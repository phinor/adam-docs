# Appendix B: Common Errors and their Meanings {#h-uakst1fvzlae}

We are slowly growing this section with errors that users come across.

## Incorrect Validation Token {#h-e7w4o1n9ydql}

### The Problem {#h-grxuhqonts75}

This error is most commonly experienced on mobile devices such as smartphones and will almost always happen after filling in a form and pressing the button at the bottom. Very commonly, this happens when logging into ADAM.

Mobile devices are especially prone to this error because fetching the page from the server will use data and so the mobile device will first try and use the same page that it had last time. If that was from a long time ago, it will include old information which will eventually expire.

ADAM checks the validation tokens to make sure that the page is new and that ADAM is not getting the contents of a very old form. If the tokens are too old, ADAM shows this error.

### How to Fix It {#h-3sk5q8j6kbdt}

The easiest way is to **refresh the page** that you are looking at before clicking on the button at bottom of the form.

If you fill in a form and then tap on the button at the bottom to move to the next step and then get this error, **move back to the page that contains the form** and **refresh that page**. On a mobile device this is commonly done by dragging down from the top of the page. This causes ADAM to get a fresh copy of the form which will contain new security tokens.

Instead of bookmarking the login page, rather bookmark the landing page once logged in. If you are logged in at that point, you won’t need to enter your password again, and if you are not, you will see the menu that will easily lead you to the login page option. By using the menu option to get to the login screen, you will almost certainly get fresh security tokens when you do so, thereby avoiding this error.

Page
