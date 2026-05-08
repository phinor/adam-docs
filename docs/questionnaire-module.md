# Questionnaire Module {#h-b6ux3wguq1hp}

ADAM includes the ability to poll teachers about pupils using standardised questionnaires. This can be used to get quick feedback on a pupil’s behaviour in class, comments about their academic performance and more.

## Overview {#h-1x72mssgpryq}

In order to use the Questionnaire module, we need to create a questionnaire, add questions to the questionnaire, distributing them to pupils and then respond to the questionnaire.

## System Administrator’s Note: Privileges {#h-346xv2x83mc1}

If you have never used the Questionnaire module before, you will need to set up privileges for the people responsible for creating questionnaires, distributing them to pupils and for responding to the questionnaires.

### Privilege Overview {#h-fdsr4zr3y601}

The Questionnaire module adds the following privileges to ADAM:

-   **Create a new questionnaire:** this privilege should be assigned to a member of staff involved at a management level with pupil affairs and pastoral matters within your school. It allows the staff member to add a new questionnaire and assign questions to it.
-   **Edit an existing questionnaire:** In order for a staff member to edit existing questionnaires, they will need this privilege.
-   **Edit questionnaire questions:** In order for a staff member to add or edit questions to a questionnaire, they will need this privilege.
-   **Assign pupils to questionnaires for completion:** This privilege should be given to grade controllers or teachers in charge of pupils in a pastoral capacity. This privilege allows those teachers to choose a particular questionnaire and ask teachers to complete it for a certain pupils.
-   **Respond to questionnaires:** This privilege should be assigned to all teachers who will need to complete questionnaires. We recommend giving this privilege to the “General Teacher” privilege group.
-   **View questionnaire summaries:** This privilege should be given to people who need to see summary reports of the questionnaires that were answered.

Example: We recommend assigning the first three privileges to a teacher in charge of pupil affairs. The fourth privilege to the grade controllers, the fifth to all teachers and the last to grade controllers.

### Assigning Privileges {#h-a6s4fyhllod5}

Individual privileges are assigned to security groups. Staff may belong to one or more security groups. The privileges are additive and cannot be taken away. Thus if a staff member is given the privilege in one security group, they cannot have it removed by another group that they belong to.

1.  To edit the security groups, click on the “**Administration**” tab, and under the “**Security Administration**” heading, click on “**Edit a security group**”.
2.  The Questionnaire privileges are in the “**Pupil Administration**” section.
3.  Once the necessary privileges have been assigned to the group, click on the “**Save Privilege Group**” button.

## Creating a Questionnaire {#h-k8pup0s4k72v}

In the “Pupils” tab, under the “Questionnaires” heading, click on the “Manage Questionnaires” link. A screen will be shown giving you options to manage the questionnaires. If you have no questionnaires, click on the “Add new questionnaire” link to get started.

You will be required to enter a **name** for the questionnaire, an optional description for it and, importantly, all the subjects that the questionnaire is applicable for. For example, if you are surveying the staff on pupils’ participation in sport, you would select only the sports from the list. If it was to do with languages, perhaps you would select only the languages from the list of subjects. Remember that you can select multiple values using “Ctrl” and “Shift” to select multiple values.

Click on “Save this questionnaire” when done.

## Managing Questions {#h-zgq55q2aexpj}

Once you have added a new questionnaire, you will immediately be taken to the “Questionnaire questions” screen. You can also get to this screen by following the menu item on the “Pupils” tab and then clicking on “Manage Questionnaire” under the “Questionnaires” heading. In the table of questionnaires that is shown, click on “questions” in the “Actions” column.

To start, click on “Add a new question”.

ADAM allows five types of questions in the questionnaire:

-   **Rating:** A rating question is rated from 1 to 5. Use the “Explanation” field to indicate what the 1 to 5 scale means.
-   **Comment:** A free-form block for paragraph answers.
-   **Yes or No:** A yes-or-no option.
-   **Number:** A numeric entry option which displays options from 0 to 100.
-   **Options:** This allows you to build your own option selectors. To add your own options, type each option separated by a comma in the “Options” block. So you could enter the values “Always, Often, Sometimes, Never” as possible options.

In the list of questions, you can click on “edit” to change the questions, “delete” to remove the question from the database, or “up” and “down” to change the order of the questions in the questionnaire.

## Assigning the Questionnaire to Pupils {#h-ek48kjz3200r}

ADAM allows you to assign the questionnaire to an entire class at a time, or to individual pupils. If you have all your pupils in grade groups, then you can assign the entire grade to have questionnaires filled in. All teachers who teach those pupils in subjects which were selected for the questionnaire will receive notifications to complete the questionnaires for those pupils.

The two options can be found on the “Pupils” tab under the “Questionnaires” heading. They are “Assign a questionnaire to a pupil” or “Assign a questionnaire to a class”.

ADAM will prompt for a deadline date. ADAM will remind teachers about any outstanding questionnaires that they might have until the deadline is past. A daily email is sent as well as notice that is displayed on the welcoming screen.

## Completing the Questionnaires {#h-wvdj8zhx6fzj}

Completing the questionnaires is straightforward for teachers. Care should be taken to set up the questions carefully so that they are not ambiguous!

From the login screen, teachers can click on the “Complete them now” link, or click on the “Complete questionnaires” link provided on the “Pupils” tab under the “Questionnaires” heading.

A list of open questionnaires will be displayed. Teachers can fill them in individually by clicking on the “respond” link next to the name of the appropriate student. If they have already filled in the questionnaire, they can edit their answers by clicking on the “edit” link next to the name of the pupil.

Alternatively, there is a link at the top of the table which allows teachers to complete all outstanding questionnaires. Click on the “one after the other” link at the top of the table. In this case, instead of returning to the table after each questionnaire, the teacher will simply be presented with the next questionnaire.

They do not have to fill them all in. ADAM will resume from where they left off when they next login.

## Viewing the Results {#h-7jfihmiqgbpc}

If teachers have the necessary privileges (see the privileges section above), they will be able to see the results of the questionnaires. To see the results of the questionnaires for a particular pupil, teachers can go to the “Pupil Info” page for a pupil and click on the “Questionnaires” header to get to that section. A list of the completed questionnaires will be shown. If a teacher did not complete a questionnaire for a pupil, their subject will not be listed.
