# Cron Service

The Cron service runs every 5 minutes to ensure that background process happen in ADAM. Such processes include:

1.  Regular database snapshots
2.  Processing the messaging queue
3.  Recalculating of changed marks

It is important that the cron service runs regularly. ADAM will notify system administrators by way of an error message on the login page if the cron process has not run for at least 10 minutes:

![](assets/screenshots/cron-service/cron-service-01.png)

## Setting up the Cron Service

### Linux Servers

The following commands should be run to set up the crontab server by an authorised sudo user:

```bash
sudo crontab -l -u www-data > ~/tempcron
sudo sed -i "/adam\\/cron\\.php/d" ~/tempcron
echo "\* \* \* \* \* php /var/www/adam/cron.php > /dev/null" >> ~/tempcron
sudo crontab -u www-data ~/tempcron
rm ~/tempcron
```

In order, these commands will:

1.  Get a list of all existing crontab services for the user www-data, stored in a temporary file called “tempcron”.
2.  Remove any lines with “adam/cron.php” in them.
3.  Add in the command to run ADAM’s cron task evert 5 minutes. Note that this command assumes that there is only a single school running on the server who’s configuration is located in the “config.ini” file. If this is not the case, please contact us for more information!
4.  Load the modified cron services.
5.  Remove the temporary file.

### Windows Servers

!!! warning
    ADAM is not supported on a Windows server.

## Ping Process

One of the background tasks that cron keeps running is the Ping process. Every so often, ADAM contacts our Ping server to report certain statistics, to check for updates and to validate the current server’s licence to operate.

Mostly, there is nothing to do - the Ping process does not normally require any human intervention!

However, if you see any errors on the login landing page relating to the ping service, administrator intervention may be necessary.

![](assets/screenshots/cron-service/cron-service-05.png)

This error will show if ADAM is not able to contact the Ping server for at least 4 hours.

### Things that can go wrong with the ping process

#### The ADAM server has no internet access

If the ADAM server is not able to connect to the internet, it cannot contact the Ping server and thus cannot validate the operating licence.

ADAM cannot validate the licence at least once in the preceding 7 day window, ADAM will assume that the licence has expired and block access to the server.

#### The Cron Process is not running

If the cron process is not running, then the Ping process cannot run. Check for any “cron status” errors on the login landing page.

![](assets/screenshots/cron-service/cron-service-06.png)

#### The ADAM Server is not able to query DNS

If the ADAM server cannot lookup the IP address of the Ping server, it won’t be able to contact the server. If this is the case, ADAM will often be unable to send email. Check that mail can be sent from the ADAM Messaging Centre.

#### The Ping Server may be down

You can check on the status of the Ping server here: [https://status.adam.co.za/780189792](https://www.google.com/url?q=https://status.adam.co.za/780189792&sa=D&source=editors&ust=1778246675918851&usg=AOvVaw05K7eTGIkb5HfDDmdkQlWr)
