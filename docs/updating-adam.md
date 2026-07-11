# Updating ADAM

Updates for ADAM are released regularly - at least twice per month and even up to once per day, depending on the reason for the update. Most updates are applied automatically overnight and do not require any user intervention. The process below is only for updates that are not applied automatically and, if there is such an update, you will receive an email warning you of such in advance of the update being made available.

Notifications of large updates with significant changes in functionality are communicated via our mailing list. If you would like to be added to the mailing list, please ask us! Send an email to [help@adam.co.za](mailto:help@adam.co.za).

## Applying Updates Manually

Most updates are applied automatically without any intervention required from you. However, it is useful to know how one can apply an update if it is required for an urgent change.

### Applying database updates

Some updates include changes to the structure of the database. These database updates are applied on the ADAM server using ADAM’s command-line tools. They are **not** applied through the web interface, and they are no longer applied automatically when you log in or by the overnight cron service.

!!! warning
    While database updates are pending, ADAM is unavailable to everyone using it through a web browser. Anyone who visits the site sees an “ADAM is being upgraded” page reading *“The database is being updated to a new version. Please try again shortly.”* (an HTTP 503 response). The site becomes available again automatically as soon as the pending updates have been applied.

To apply the pending database updates:

1.  Log in to the ADAM server over SSH as a user that is permitted to run ADAM’s command-line tools.
2.  Change to the ADAM installation directory (for example, `/var/www/adam`).
3.  Check which updates are pending:

    ```bash
    php adam schema:status
    ```

4.  Apply the pending updates:

    ```bash
    php adam schema:migrate
    ```

5.  ADAM lists each update as it is applied and confirms when the database is up to date. Once the command has finished, the web interface becomes available again automatically.

!!! note
    On servers with an automated deployment process, `php adam schema:migrate` runs as part of each deployment, so pending database updates are normally applied for you. You only need to run it by hand if a deployment did not complete, or when the ADAM support team asks you to.

### To apply an update file sent by email

1.  Save the attachment from the email to your computer.
2.  Log into ADAM using an administrator account with the necessary privileges from any computer with Internet access.
3.  Navigate to "Administration" → "Updates" → "Apply ADAM Update".
4.  Browse to find the file you saved and upload it.
5.  ADAM will double-check to ensure that you have not skipped an update or are attempting to apply updates in the wrong order. ADAM will then apply the update.
6.  Please wait for the summary report to be shown. ADAM will show you any inconsistencies that might exist between your server and the manifest that was included in the update.
7.  Please log out of ADAM and log back in again with your administrator account.

!!! note
    If the update includes database changes, apply them from the server afterwards by running `php adam schema:migrate`, as described under [Applying database updates](#applying-database-updates) above.
