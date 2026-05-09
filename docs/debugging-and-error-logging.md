# Debugging and Error Logging

System administrators are able to have a look at ADAM’s error logging. This is useful when reporting errors to the ADAM Helpdesk ([help@adam.co.za](mailto:help@adam.co.za)). There are two aspects to the error logging: SQL errors and PHP errors.

## SQL Errors

SQL errors occur infrequently. When they happen, a user might notice a red “E1” at the bottom of the screen in the debug panel. System administrators will see a blue “E0” under normal circumstances and a red E when an error occurred. The “0” means no errors, whereas “E1” would mean 1 error occurred, “E2” would mean 2 errors occurred and so on. System administrators can click on this error code to see a list of the errors that have been logged, either from SQL or from debugging code. There are some filters at the top that can be used to narrow down the list.

This screen also contains a link to see the contents of the PHP error log file.

!!! warning
    The error log will only keep entries from the last 90 days. Thus system administrators do not have to worry about this data taking up too much space.

