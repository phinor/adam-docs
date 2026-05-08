# Onboarding Process {#h-yzua0mmt5o98}

Welcome to ADAM!

Moving to a new administration system can be a daunting taks and we want to make it as seamless as it possibly can be. This section in our documentation is written with new schools in mind who’ve just made the decision to sign up with ADAM. What follows is the process required by new schools (or most of them!) to ensure a smooth transition to ADAM.

## Customer Information {#h-lhmktfdmhgr4}

Firstly, we need to know a bit about you. You will be sent a link to an online form that asks for various bits of information so that we can draw up a Service Level Agreement for you and create a profile on our accounting package.

## Service Level Agreement {#h-na7pblyr84j7}

We will then draw up a Service Level Agreement (SLA). The terms of the agreement will be sent to you for your comment and signature. The SLA will include the standard terms and conditions of service, as well as detailing the costs that you will incur for licence fees over the first (calendar) year of using ADAM. These should match the quotations that you would have received from us unless we have specifically discussed alternative terms.

If you are happy with the terms of the agreement, you can sign and return the form to us. It will be countersigned and a copy returned to you.

Now it’s official!

## Server Setup {#h-gdxbr0kw2kbi}

You will have decided by now whether you will want us to host your ADAM server in the cloud, or whether you would like to self-host. The process is different depending on which option you have chosen, but we will still need some information before we can begin the configuration process.

### Information Required {#h-hrpw5jv2fmce}

-   The domain name you will want to use.

-   We can provide you with a “something.adam.co.za” address, but many schools prefer to have ADAM appear under their own domain name: “adam.school.co.za”. The choice is yours to make and there are no advantages one way or another.
-   If you wish to make use of your domain name, your Internet Service Provider or Domain host will need to configure an entry in your “Zone” file.

### Option A: Cloud Hosted {#h-fqifj8eewvmu}

The good news is that there is very little to do here. We will take care of the setup and getting a fresh ADAM database ready for you.

Depending on your domain configuration (see above!) you may need to ask your Domain host to create a CNAME entry to point to a domain that we will tell you.

### Option B: Self-Hosted {#h-hiximb314lu0}

If you have chosen to “self-host” ADAM, we will now make arrangements with your IT department to explain the requirements for the new server.

These will include:

-   Installation of the latest Ubuntu LTS Server version (normally on a VM)
-   Firewall configuration: access for SSH communication (to allow for initial server configuration), HTTP and HTTPS.
-   Local DNS configuration.

Depending on your domain configuration (see above!) you may need to ask your Domain host to create either an “A” record or “CNAME” record in your Zone file to point most commonly to your external IP address.

## Initial Configuration {#h-hzr8v3r7mrar}

Once the server is up and running, there are a few initial things that we need to set up and configure.

-   Email

-   ADAM uses external mail services to deliver mail. Many schools with Google Workspace Mail or Microsoft 365 use that infrastructure for ADAM to deliver mail. Other schools make use of external SMTP service providers to deliver mail on their behalf.
-   If you want to send mail via [Google Workspace Mail](communication-settings-in-adam.md#h-8wr08et4phui) or [Microsoft 365](communication-settings-in-adam.md#h-81whw3364cwf), there are configuration changes that must be made in your management consoles for each service. Details on these configuration requirements can be found at the links above.

## Data Import {#h-42oscyqqpai2}

On signing the SLA, we will have sent a template as an example for importing the data. It may take some time to compile this data and so our advice is to get busy with that as soon as you can. We can only begin the import once the data has been provided to us.

Our standard operating procedure is to import information related to pupils, families and staff. Any further academic information can be imported, but this is only done by special arrangement.

## Training {#h-8muf1qd4qnb}

We like to wait until your data is imported before beginning training on ADAM. This is because it is helpful to have a familiar context when learning a new system.

Training is generally done in four online sessions of two hours each. When we arrange the training we will provide a breakdown of what each section entails and give some guidance on which staff members should attend each session. Ideally, the training should be aimed at champions within your school who are then better positioned, within your school’s unique context, to train other staff.
