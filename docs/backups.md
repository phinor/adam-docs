# Backups

## Database Snapshots

ADAM will create snapshots of the database at predefined times during the day. Snapshots are kept for differing lengths of time:

-   Daily snapshots: usually taken twice per day. ADAM keeps the 14 most recent.
-   Weekly snapshots: taken every Monday morning. ADAM keeps the 4 most recent.
-   Monthly snapshots: taken on the 1st of every month. ADAM keeps the 12 most recent.
-   Yearly snapshots: taken before the year-end roll-over is completed. Kept indefinitely.

The numbers of backups and the frequency that the daily backups are taken are controlled in the **Site Settings** on the **Backups & Maintenance** tab under the **Snapshots** heading.

These backups are not much use by themselves. They exist on the same machine as the actual database and so if there is a physical machine failure, it is possible that your backups will be lost too. For this reason, it is incredibly important that your backups are copied to a different physical machine at the very least.
