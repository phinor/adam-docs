# Change History Reports

ADAM keeps an audit trail of two areas that were previously hard to review after the fact: changes to your **staff security groups** and changes to your **site settings**. Each area has its own history report, described below.

These reports only show what has happened – they are read-only. They do not let you undo a change, but they do let you see exactly who did what, and when.

## Group Change Audit

Whenever a staff security group is created, renamed, disabled, locked, or has its members or permissions changed, ADAM records the change. The Group Change Audit report lets you review this history.

To open the report, navigate to **Administration → Change Log → Group changes (audit)**.

![](assets/screenshots/change-history-reports/change-history-reports-01.png)

The opening page is split into two lists:

- **By group** – a list of every staff group. Click a group to see its full change history.
- **By staff member who made changes** – a list of every staff member who has made a group change. Click a name to see everything that person changed.

### Viewing a single group's history

Choosing a group from the **By group** list shows that group's changes in date order.

![](assets/screenshots/change-history-reports/change-history-reports-02.png)

The table has three columns:

| Column | Meaning |
| ------ | ------- |
| **When** | The date and time of the change. |
| **Change** | A plain-language description – for example, a member being added or removed, a permission being granted or revoked, the group being renamed, disabled, or locked. |
| **By** | The staff member who made the change. Automatic changes made by ADAM itself are shown as **System**. |

!!! tip
    You can also reach a group's history directly from the group list. Navigate to **Administration → Staff Groups → Manage staff groups** and click the **history** (clock) icon next to a group. When you open the history this way, the **Back** button returns you to the group list rather than to the audit report.

### Viewing changes by a staff member

Choosing a name from the **By staff member who made changes** list shows every group change made by that person.

![](assets/screenshots/change-history-reports/change-history-reports-03.png)

This view adds a **Group** column so you can see which group each change affected. Because a single person may have made a great many changes, this view also offers a date filter. Enter a **From** and **To** date and time and click **Filter** to narrow the list to a particular period.

!!! note
    The Group Change Audit is available to staff who hold the **Manage Staff Group Permissions** permission – the same permission that allows a user to change a group's permissions in the first place. If you cannot change group permissions, you will not see this report.

## Site Settings History

Every change to a site setting is recorded, and super administrators can review the full audit trail.

To open the report, navigate to **Administration → Change Log → Site settings history**.

![](assets/screenshots/change-history-reports/change-history-reports-04.png)

The table lists every setting change, newest first:

| Column | Meaning |
| ------ | ------- |
| **Time and Date** | When the setting was changed. |
| **Setting** | The section and name of the setting that changed. |
| **Old Value** | The value before the change. |
| **New Value** | The value after the change. |
| **Changed By** | The staff member who made the change. |

!!! warning
    Secret settings – such as passwords – are never written to the history, so their values are not exposed here.

!!! note
    The Site Settings History page is visible to **super administrators** only.

Separately from this report, ADAM also e-mails a digest whenever a site setting changes, so that administrators are alerted even if they do not check the history page. See [Changing Site Settings](changing-site-settings.md) for more on the settings themselves, and [Change Log Notifications](change-log-notifications.md) for how to watch individual settings for change alerts.
