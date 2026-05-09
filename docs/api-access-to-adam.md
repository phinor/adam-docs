# API Access to ADAM

## Introduction the ADAM API

An API allows for another computer program to connect to ADAM to either access data stored in its database or to make
changes to that data. ADAM makes use of a “RESTful” API and returns data mostly in JSON format.

### What is a RESTful system?

REST is a technique of communicating with an API which is very common amongst web-based applications - such as ADAM.
Other programs will make one of four types of web request depending on what they are hoping to do in the database, and
include the necessary information for ADAM. ADAM then responds to that request with the appropriate data or success
code.

### How does access control work?

Access to the ADAM database is controlled using a token system. These are essentially random passwords that are created
which are shared only with the other program that wishes to access the API. Because these tokens are really only meant
to be used by a computer, it is not important that they are memorable or easy to type. In fact, ADAM will generate a
random set of characters to be used as the API key and you are strongly encouraged to make use of the suggested token.

It is vitally important that the token is kept confidential between the person issuing it and the person using it.
Anyone who knows the token will be able to access the API. Please read
the [Best Practices](#best-practice-security-principals) section below for further information.

Each API token can be given access to one or more [API resources](#api-resources). Anyone who knows the API token can
access all the resources that have been allocated to that token.

API tokens can be revoked at any point and can have their resources changed and added to over time. Any changes you make
to the token and its API resource assignments will take place immediately.

## Managing API Tokens in ADAM

In ADAM: Navigate to **Administration → Security Administration → Manage API Tokens**.

A list of existing API tokens will be shown. Click on **Add new API Token** to begin the process of creating a new
Token.

![](assets/screenshots/api-access-to-adam/api-access-to-adam-01.png)

1. A random 30-character **token** will be generated. This should be left unmodified unless you have a very specific
   reason to do so. Once set, token values cannot be changed. If you need to change the token, you must delete the
   existing endpoint and create a new one.
2. Select the appropriate **resources** to allow the token to access. Hold down the “Ctrl” key on your keyboard to allow
   you to select multiple resources by then clicking on those resources while holding down that button.
3. Add **notes** if required. It is a good idea to make note of what service is making use of the API token.
4. Click on **Save Token**.

!!! warning
The random 30 character token must be kept secret since will will allow anyone who knows it access to the data stored in
the ADAM database. It will need to be shared with the integration provider and great care should be taken with how they
are provided the API key. We strongly recommend against sending this information via email or other unsecured means.

### Managing Existing Tokens

In the table of existing API tokens, you have the option to **edit**, **delete** or **regenerate** the API token.

**Edit** allows you to change the **Resources** and **Notes** associated with an endpoint, but does not allow you to
edit the Token.

**Regenerating** a token will create a new random value for the token but will keep your resources and notes the same.
If you do regenerate a token, please remember to update your external systems with the new token.

**Deleting** the token will remove it from the list and it will no longer be available for use. Systems that rely on the
resources will no longer have access to the data supplied by ADAM.

## Best Practice Security Principals

The following are provided as best practice guidelines for managing API tokens.

1. Treat API Tokens as **top secret**. Do not send them via email and do not publish them in a place where they could be
   accessed by unauthorized personnel. API access can expose sensitive data. Allowing an API tokens to fall into the
   wrong hands could expose personal information about the users of your system and this would be considered an offence
   under the “Protection of Personal Information Act” (POPIA). Access to such personal information could become a
   security and safety issue.
2. Each entity (e.g. a program that is accessing data from ADAM) should have its **own** token or tokens. Tokens should
   never be shared between entities. If another entity requires access to the same data, give it a new token. This
   allows you to revoke each token individually and stop one program from accessing the data without affecting any other
   programs.
3. Programmers integrating with the ADAM API should not, under any circumstances, include API tokens in their source
   code and should always fetch them from some form of access controlled data storage.

## API Interactions

### Authentication

All API requests should be authenticated using a Bearer Token.

**Example:**

Authenticating with the token value svyzBvkuuXLdJwV7YcdYsQFVX5ha54 would yield the following header:

```
Authorize: Bearer svyzBvkuuXLdJwV7YcdYsQFVX5ha54
```

ADAM also will accept a Basic Authorization header with an arbitrary username. Authenticating with the username apitoken
token value `svyzBvkuuXLdJwV7YcdYsQFVX5ha54` would yield the following header:

```
Authorize: Basic YXBpdG9rZW46c3Z5ekJ2a3V1WExkSndWN1ljZFlzUUZWWDVoYTU0
```

### API Requests

All API requests, as listed below, should be prefixed with the “api” folder to make the URL end-point:

```
https://*adam.example.com*/api/
```

The remainder of the URL generally consists of a module name, a data set and zero or more parameters. These should all
be in lower-case. For example:

```
https://demo.adam.co.za/api/request/test/parameter
```

Parameters should
be “[percent encoded](https://www.google.com/url?q=https://www.w3schools.com/tags/ref_urlencode.asp&sa=D&source=editors&ust=1778246675609863&usg=AOvVaw3YqxCg2gCwh23giGyigZmH)”.
Spaces should be encoded as %20 and not as a “+”.

A `GET` request to this API end-point would require token access to the resource: request/test:get. Note that without
specifically assigned access, access to the resource - even this test resource - will be denied.

### API Responses

All responses will be returned within JSON objects. The basic structure of these objects is:

```json
{
  "data": null,
  "message": "",
  "response": {
    "error": "",
    "code": 200
  }
}
```

Any response which does not have these properties as listed above, MUST be treated as invalid.

The contents of the **data** attribute will depend on the API endpoint being interrogated.

The **message** attribute contains a human-readable message which, in most cases, describes the data set that has been
returned. This is intended for debugging and may change unpredictably with future versions of ADAM.

The **response code** should mirror the HTTP response code which will be descriptive of the success or failure of the
call. The **error** attribute will provide a human-readable description of the error. The error message is not intended
to be interpreted by machines.

## API Resources

These are the available documented resources. Other resources are available but are not listed here until their
development is complete and considered stable.

### AbsenteeKiosk/register:post

This registers a pupil as either present or late. It is intended to be used either by automated access control systems
or ADAM’s own absentee kiosk.

#### Request

- `POST` to `/api/absenteekiosk/register/<pupil>`
- `POST` to `/api/absenteekiosk/register` with `pupil=<pupil>` as a form variable in the POST body

#### Parameters

- `<pupil>`: The ADAM identifier of the pupil.

#### Response

If the pupil identifier can be matched against an existing pupil, the endpoint will return two items in the data object.
These are used internally by ADAM’s “Absentee Kiosk” feature.

- `message`: an HTML message which will contain the name of the pupil and confirmation that they have been registered.
- `colour`: an HTML hex code either red, green or amber depending on the status.

The times and windows are configured in ADAM’s site settings. Depending on these settings, ADAM will report one of the
following HTTP status codes:

- The pupil identifier is not recognised: `404 (Not found)`
- The pupil is too early and registers before the earliest time allowed: `406 (Not acceptable)`
- The pupil registers during the first window and is recorded as present: `200 (OK)`
- The pupil registers during the second window and is recorded as late: `202 (Accepted)`
- The pupil is too late and registers after the second window closes: `406 (Not acceptable)`

In each case, the status code will be corroborated by a more descriptive message.

**Example:**

```json
{
  "data": {
    "message": "<strong>Joe Smith</strong> has been recorded as <strong>present</strong>",
    "colour": "green"
  },
  "message": "",
  "response": {
    "error": "Present",
    "code": 200
  }
}
```

### Absentees/summarycount:get

Returns a list of pupils and the number of days they’ve been absent. This counts all the absentees with a reason that is
set to count as “absent”. Only pupils with absentee records are returned. All pupils, including those that might have
left the school, are returned.

#### Request {#absenteessummarycountget-request}

```
GET /api/absentees/summarycount/<from>[/<to>]
```

#### Parameters {#absenteessummarycountget-parameters}

- `<from>`: An ISO formatted date to begin the summary. This date is included in the summary.
- `<to>`: OPTIONAL. An ISO formatted date to mark the end of the range of the summary. This date is included in the
  summary. If omitted, the current date is used instead.

#### Response {#absenteessummarycountget-response}

The data attribute will be an array of zero or more JSON objects.

**Example:**

```
GET /api/absentees/summarycount/2018-01-01/2018-01-31
```

```json
{
  "data": [
    {
      "pupil_id": 875,
      "pupil_admin": "19634",
      "absent_count": 1
    },
    {
      "pupil_id": 879,
      "pupil_admin": "52351",
      "absent_count": 2
    }
  ],
  "message": "Absentee counts for all pupils from 2018-01-01 to 2018-01-31.",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

- `pupil_id` is ADAM’s internal database identifier and will always refer to a unique pupil.
- `pupil_admin` is the user-defined administration number. While this should not change, it may do so at the school’s
  discretion.
- `absentee_count` is the number of days that the pupil has been recorded as absent. This does not include absentee
  records which do not prejudice a pupil (such as “away on sports tour”). These reasons are customisable by the school.

### Absentees/list:get

Gets a list of pupils absent with the reasons.

#### Request {#absenteeslistget-request}

```
GET /api/absentees/list/[<date>[/<to>]]
```

#### Parameters {#absenteeslistget-parameters}

- `<date>`: OPTIONAL. An ISO formatted date to query the absentees. If omitted, today’s date is used.
- `<to>`: OPTIONAL. An ISO formatted date. If provided, all absentees on or between the `<date>` and `<to>` dates will be
  provided. If omitted, `<to>` effectively takes the same value as `<date>` and only absentees for that date are provided.

#### Response {#absenteeslistget-response}

```
GET /api/absentees/list/2018-01-30
```

```json
{
  "data": [
    {
      "pupil_id": 1720,
      "pupil_admin": "47547",
      "absent_date": "2018-01-31",
      "absent_reason_id": 1,
      "absent_reason_description": "Absent",
      "absent_notes": "App Test"
    }
  ],
  "message": "Absentee list for all pupils from 2018-01-31 to 2018-01-31.",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

The data attribute contains an array of zero or more absentee records. Each record is a JSON object with the following
properties:

- `pupil_id` is ADAM’s internal identifier for the pupil.
- `pupil_admin` is a school-provided identifier for the pupil. While this should not change, it may do so at the
  school’s discretion.
- `absent_date` gives the date that the absentee occurred on in case a range of dates was requested. A pupil can only
  have a single absentee record per day.
- `absent_reason` is an internal identifier corresponding to the absentee reason that was chosen.
- `absent_reason_description` is the descriptor for the absentee reason. It will be consistent per `absent_reason` in
  any one API call, but may change between calls at the school’s discretion.
- `absent_notes` contain the end-user provided notes related to the pupil’s absence. This may contain personal
  information.

### Absentees/daysabsentforpupil:get

Returns the absentee log for a specific pupil.

#### Request {#absenteesdaysabsentforpupilget-request}

```
GET /api/absentees/daysabsentforpupil/<pupil>/<year>
```

#### Parameters {#absenteesdaysabsentforpupilget-parameters}

- `<pupil>`: ADAM internal pupil identifier (required)
- `<year>`: Calendar year to filter by (optional; returns all records if omitted)

#### Response {#absenteesdaysabsentforpupilget-response}

Data attribute contains the pupil's absentee log entries.

### Admin/test:get

Internal test endpoint for verifying API connectivity.

#### Request {#admintestget-request}

```
GET /api/admin/test
```

#### Parameters {#admintestget-parameters}

None.

#### Response {#admintestget-response}

```json
{
  "data": "Successfully fetched data by asynchronous call from the server at 2026-04-09 14:30:00",
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Applications/applicationformfields:get

The ability to see which fields are accepted as part of the application form. These fields can be customised by updating
the core and custom fields to change their availability in the application form.

#### Request {#applicationsapplicationformfieldsget-request}

```
GET /api/applications/applicationformfields
```

#### Parameters {#applicationsapplicationformfieldsget-parameters}

None

#### Response {#applicationsapplicationformfieldsget-response}

The output data will be a JSON object containing the fields that are accepted. Within the data property are two sub
arrays for families and pupils. These list the field names that are accepted.

**Example:**

```
GET https://demo.adam.co.za/api/applications/applicationformfields
```

```json
{
  "data": {
    "families": [
      "family_primary_idnum",
      "family_primary_lastname",
      "family_primary_firstname",
      "family_primary_fullfirst",
      "family_primary_title",
      "family_primary_initials",
      "family_primary_gender",
      "family_primary_birth",
      "family_primary_occupation",
      "family_primary_employer",
      "family_primary_workphone",
      "family_primary_cell",
      "family_primary_cell_sms",
      "family_primary_email",
      "family_secondary_idnum",
      "family_secondary_lastname",
      "family_secondary_firstname",
      "family_secondary_fullfirst",
      "family_secondary_title",
      "family_secondary_initials",
      "family_secondary_gender",
      "family_secondary_birth",
      "family_secondary_occupation",
      "family_secondary_employer",
      "family_secondary_workphone",
      "family_secondary_cell",
      "family_secondary_cell_sms",
      "family_secondary_email",
      "family_address_residential_1",
      "family_address_residential_2",
      "family_address_residential_suburb",
      "family_address_residential_city",
      "family_address_residential_province",
      "family_address_residential_code",
      "family_address_residential_country",
      "family_address_postal_1",
      "family_address_postal_2",
      "family_address_postal_suburb",
      "family_address_postal_city",
      "family_address_postal_province",
      "family_address_postal_code",
      "family_address_postal_country",
      "family_home_phone",
      "family_home_fax",
      "family_ice",
      "family_ice_number",
      "family_report_required"
    ],
    "pupils": [
      "pupil_lastname",
      "pupil_fullfirst",
      "pupil_firstname",
      "pupil_gender",
      "pupil_idnumber",
      "pupil_birth",
      "pupil_religion",
      "pupil_population_id",
      "pupil_language_id",
      "pupil_language_other",
      "pupil_teaching_language_id",
      "pupil_entry",
      "pupil_final",
      "pupil_email",
      "pupil_cell",
      "pupil_cell_sms",
      "pupil_allergies",
      "pupil_medaid_name",
      "pupil_medaid_number",
      "pupil_medaid_principal",
      "pupil_medaid_principal_id",
      "pupil_doctor",
      "pupil_doctor_phone",
      "pupil_orphan_status",
      "pupil_relationships",
      "pupil_atschool",
      "pupil_prevschool_firstprovince",
      "pupil_prepschool",
      "pupil_prevschool_country",
      "pupil_prevschool_formalgrr",
      "pupil_nationality",
      "pupil_studypermit_required",
      "pupil_studypermit",
      "custom_38",
      "custom_36"
    ]
  },
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Applications/apply:post

Submit an application to the site. Note that if the ID number submitted matches an existing parent, the child will
automatically be linked to that parent. Note that when applications are submitted through ADAM’s web interface, ADAM
automatically authenticates the parent to ensure that strange children are not linked to their profiles. Implicit in the
web application is the validation of the email address which is done as part of the application process. Applications
received via the API are not given such scrutiny and special care should be taken on the sending system to mitigate
against spam and fraudulent attempts at applications.

#### Request {#applicationsapplypost-request}

```
POST /api/applications/apply
```

#### Parameters {#applicationsapplypost-parameters}

None - data sent by message body.

#### Body

The body of the request should contain the data required for the application. The data should either be in JSON format,
or as an encoded query string (as is typical with normal form-submitted data).

Fields: The three fields, `idnumber`, `email`, and `phone`, may be duplicated within the parent information. It is not
necessary that they complete them twice, but it is necessary for the information to be submitted both with the family
and as separate information.

Note carefully the point about existing parents: *if their ID or passport numbers already exist in ADAM’s database, the
family information provided in the application will be silently discarded in favour of information already in the
database.* Thus having updated contact information provided in the email and phone fields is important. The silent
discarding is to ensure that malicious actors cannot update family information without their authorisation.

- `idnumber`: The South African ID or passport number of the parent making the submission. This is used to match against
  other families. If omitted, no linking will take place. If this value matched the value of an existing family, the
  pupil will automatically be linked to that family and the information provided in the family info will be lost.
- `email`: The email address to get in tough with the parents regarding the application.
- `phone`: The phone number to get in touch with the parents regarding the application.
- `application`: The body of the application. This contains:

    - `pupil`: An array of child information to be included on the application. Each element of the array is a sub-array
      of information for each child. A valid application must have at least one child and no more than 5 children.
    - `family`: An array of family fields to be included.
    - `email`: further details of the parents’ email addresses.

A minimum set of required fields is:

- Families:
    - Primary last name (`family_primary_lastname`)
    - Primary first name (`family_primary_firstname`)
    - Primary full first names, can duplicate `family_primary_firstname` if required  (`family_primary_fullfirst`)

- Pupils:
    - Last name (`pupil_lastname`)
    - Preferred name (`pupil_firstname`)
    - Full first name, can duplicate pupil_firstname if required (`pupil_fullfirst`)
    - Gender (`pupil_gender`)
    - Year of entry (`entry_year`) - note non-standard field naming
    - Month of entry (`entry_month`) - note non-standard field naming
    - Grade of entry (`entry_grade`) - note non-standard field naming. Note, integers accepted only. For grades prior to
      Grade 1, zero or negative grades: Grade R = 0, Grade RR = -1, Grade RRR = -2, etc.

##### Example (JSON):

```json
{
  "idnumber": "1234567890123",
  "email": "morticia@adam.co.za",
  "phone": "0834699569",
  "application": {
    "pupil": [
      {
        "pupil_lastname": "Addams",
        "pupil_firstname": "Wednesday",
        "pupil_fullfirst": "Wednesday Jane",
        "pupil_gender": "Female",
        "entry_year": "2019",
        "entry_month": "1",
        "entry_grade": "10",
        "relationship": [
          {
            "primary": "biological",
            "secondary": "step parent"
          }
        ]
      },
      {
        "pupil_lastname": "Addams",
        "pupil_firstname": "Pugsley",
        "pupil_fullfirst": "Pugsley Georgie",
        "pupil_gender": "Male",
        "entry_year": "2019",
        "entry_month": "1",
        "entry_grade": "8",
        "relationship": [
          {
            "primary": "step parent",
            "secondary": "biological"
          }
        ]
      }
    ],
    "family": {
      "family_primary_idnum": "1234567890123",
      "family_primary_lastname": "Addams",
      "family_primary_firstname": "Gomez",
      "family_primary_fullfirst": "Gomez",
      "family_secondary_idnum": "1234567890123",
      "family_secondary_lastname": "Addams",
      "family_secondary_firstname": "Morticia",
      "family_secondary_fullfirst": "Morticia May"
    },
    "email": [
      {
        "member": "primary",
        "address": "gomes@adam.co.za",
        "bulk": "Yes",
        "reports": "Yes"
      },
      {
        "member": "secondary",
        "address": "morticia@adam.co.za",
        "bulk": "Yes",
        "reports": "Yes"
      }
    ]
  }
}
```

#### Response {#applicationsapplypost-response}

A simple object providing notification of success or failure. The application field gives a code unique to this
application which will, in a future development, allow for editing of the application.

```json
{
  "data": {
    "application": "6ESKmQYMWH3KbJUdAESsZUi3BysaLx"
  },
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Applications/verifyid:get

Checks whether an ID number is associated with an existing family login account.

#### Request {#applicationsverifyidget-request}

```
GET /api/applications/verifyid/<idNumber>
```

#### Parameters {#applicationsverifyidget-parameters}

- `<idNumber>`: South African ID number to look up (required)

#### Response {#applicationsverifyidget-response}

No data attribute. The `response.message` field indicates the result:

- "authorization required" — ID number found and a password exists (family can log in)
- "authorization not possible" — ID number found but no password set
- "id number not found" (code 404) — no matching record

### Assessment/recentresults:get

Returns recent assessment results for a pupil.

#### Request {#assessmentrecentresultsget-request}

```
GET /api/assessment/recentresults/<pupil>
```

#### Parameters {#assessmentrecentresultsget-parameters}

- `<pupil>`: ADAM internal pupil identifier (required)

#### Response {#assessmentrecentresultsget-response}

Data attribute contains an array of assessment result objects:

```json
{
  "data": [
    {
      "assessment_id": 42,
      "assessment_period_id": 3,
      "assessment_description": "Term 1 Test",
      "assessment_date": "2026-03-15",
      "assessment_releasedate": "2026-03-20",
      "assessment_total": 100,
      "assessment_weighting": 1.0,
      "assessment_weighting_display": "10%",
      "result_total": 78,
      "result_comment": "",
      "class_grade_id": 10,
      "class_description": "10A",
      "subject_name": "Mathematics",
      "subject_short": "Maths"
    }
  ]
}
```

### Questions/questionbreakdown:get

Returns a per-question breakdown of a pupil's assessment results.

#### Request {#questionsquestionbreakdownget-request}

```
GET /api/questions/questionbreakdown/<pupil>/<assessment>
```

#### Parameters {#questionsquestionbreakdownget-parameters}

- `<pupil>`: ADAM internal pupil identifier (required)
- `<assessment>`: Assessment identifier (required)

#### Response {#questionsquestionbreakdownget-response}

Data attribute contains an array of question result objects:

```json
{
  "data": [
    {
      "question_description": "Algebra",
      "outcome_name": "Patterns and Algebra",
      "answer_total": 8.5,
      "answer_level": "B",
      "question_total": 10
    }
  ]
}
```

### Calendar/pupillinks:get

This provides calendar subscription links for all current pupils. API keys are generated automatically for pupils who
don't have one yet.

#### Request {#calendarpupillinksget-request}

```
GET /api/calendar/pupillinks/
```

#### Parameters {#calendarpupillinksget-parameters}

None required.

#### Response {#calendarpupillinksget-response}

```
GET /api/calendar/pupillinks/
```

```json
{
    "data": [
        {
            "pupil_id": 142,
            "calendar_link": "webcal://adam.example.com/api/calendar/xK9mNp2qRs5tUv8wXy1zA4bCdEfGhIjKlMnOpQrStUvWxYz012"
        }
    ],
    "message": "",
    "response": {
        "error": false,
        "code": 200
    }
}
```

### Calendar/stafflinks:get

This provides calendar subscription links for all current staff. API keys are generated automatically for staff who don't have one yet.

#### Request {#calendarstafflinksget-request}

```
GET /api/calendar/stafflinks/
```

#### Parameters {#calendarstafflinksget-parameters}

None required.

#### Response {#calendarstafflinksget-response}

```
GET /api/calendar/stafflinks/
```

```json
{
    "data": [
        {
            "staff_id": 3,
            "calendar_link": "webcal://adam.example.com/api/calendar/gMSrVY4iGLAdk3RDks7AK3a2BTFW9PAGgpt9MgPDvVd6vBS7im"
        }
    ],
    "message": "",
    "response": {
        "error": false,
        "code": 200
    }
}
```

### Changelog/undo:post

Undoes a changelog entry, reverting a field to its previous value.

#### Request {#changelogundopost-request}

```
POST /api/changelog/undo/<changeSet>
```

#### Parameters {#changelogundopost-parameters}

-   `<changeSet>`: The changelog entry identifier (URL path parameter)

#### Response {#changelogundopost-response}

-   Code 200: Undo successful
-   Code 403: Cannot undo the original entry (no previous value to restore)
-   Code 202: Undo operation failed

### Classes/pupilteachers:get

This provides a list of classes that an individual pupil is registered for.

#### Request {#classespupilteachersget-request}

```
GET /api/classes/pupilteachers/<pupil>
```

#### Parameters {#classespupilteachersget-parameters}

-   `<pupil>` is the pupil identifier

#### Response {#classespupilteachersget-response}

```
GET /api/classes/pupilteachers/123
```

```json
{
    "data": [
        {
            "class_id": 1111,
            "class_description": "AB",
            "class_gradeyear": 10,
            "subject_name": "Geography",
            "subject_short": "Geo",
            "staff": {
                "staff_id": 321,
                "staff_lastname": "Van Der Walt",
                "staff_firstname": "Drikus",
                "staff_title": "Mr",
                "staff_email": "dvdwalt@school.example.com"
            },
            "teaching_assistants": [
                {
                    "staff_id": 1234,
                    "staff_lastname": "Smith",
                    "staff_firstname": "James",
                    "staff_title": "Mr",
                    "staff_email": "jsmith@school.example.com"
                }
            ],
            "class_friendly": "Geography Grade 10 AB"
        }
    ],
    "message": "",
    "response": {
        "error": "OK",
        "code": 200
    }
}
```

The `data` attribute contains one or more class objects. This contains the details of the subject, and the class.

Note that the `class_gradeyear` property can be negative to represent pre-school grades. (e.g. Grade 0 = Grade R, Grade -1 = Grade RR, and so on).

One `staff` member (the teacher of the class) will be provided, and the `teaching_assistants` may contain 0 or more staff objects.

### Classes/bygradeperiodsubject:get

Returns classes matching a specific grade, reporting period, and subject combination.

#### Request {#classesbygradeperiodsubjectget-request}

```
GET /api/classes/bygradeperiodsubject/<grade>/<period>/<subject>
```

#### Parameters {#classesbygradeperiodsubjectget-parameters}

-   `<grade>`: Grade identifier (required)
-   `<period>`: Reporting period identifier (required)
-   `<subject>`: Subject identifier (required)

#### Response {#classesbygradeperiodsubjectget-response}

```json
{
    "data": [
        {
            "id": 150,
            "grade": 10,
            "gradetext": "Grade 10",
            "description": "10A",
            "subject": 5,
            "fulldescription": "Grade 10 Mathematics 10A",
            "teacher_id": 42,
            "teacher_name": "Mr Smith"
        }
    ]
}
```

### Cron/cronlog:get

Returns cron job execution logs. Restricted to super-admin tokens.

#### Request {#croncronlogget-request}

```
GET /api/cron/cronlog/<cronLogID>
```

#### Parameters {#croncronlogget-parameters}

-   `<cronLogID>`: Either a numeric log entry ID (returns that specific record with full log content) or any non-numeric value (returns all records without log content)

#### Response {#croncronlogget-response}

When requesting a specific entry, returns the full cron log record including log output. When requesting all entries, returns an array of records without the log body to reduce payload size.

### DataQuery/get:get

Provides automated access to a whole-school scratch list. The contents of the scratch list fields can be customised as per the settings in ADAM found at **Administration → Security → Manage Data Query API Fields**.

Please treat this feature with the utmost care. By its very definition, it gives wide access to a range of personal data.

#### Create a Data Query Secret

To use this API endpoint, an additional data query token must be defined.

![](assets/screenshots/api-access-to-adam/api-access-to-adam-03.png)

Note that field access definitions can only be linked to a single API Token. If multiple API tokens require access to the same fields, this process must be duplicated for each API token and a unique list created for each.

-   Select the **API Token** that you want to associate with this query. *Note that only API Tokens who have access to the* *DataQuery/get/get* *resource may be selected here.*
-   Make a note of the **Secret** and do not share this with unauthorized personnel.
-   Choose a **data source** for the query. Once set here, this cannot be changed later.
-   Add a **comment** to provide insight into the function and reason for this query.

Click on **Add record** when done.

A second screen will show, allowing you to select the fields required for this query:

![](assets/screenshots/api-access-to-adam/api-access-to-adam-04.png)

Check the fields that you require and **save** your selections using the button at the bottom.

#### Request {#dataquerygetget-request}

```
GET /api/dataquery/get/<secret>
```

OR, for a modified data structure to provide more consistency for automated systems, (see example response below), add the version parameter “2” to the end of the request.

```
GET /api/dataquery/get/<secret>/2
```

#### Parameters {#dataquerygetget-parameters}

-   `<secret>` is a series of random characters as [created above](#create-a-data-query-secret).

#### Response {#dataquerygetget-response}

```
GET /api/dataquery/get/GXiE4V5qYB
```

```json
{
    "data": {
        "49": {
            "admin_number_1": "3316",
            "lurits_number_177": "",
            "age_6": "15 years, 200 days",
            "gender_10": "Male"
        },
        "4688": {
            "admin_number_1": "6333",
            "lurits_number_177": "",
            "age_6": "17 years, 10 days",
            "gender_10": "Male"
        }
    },
    "message": "",
    "response": {
        "error": "OK",
        "code": 200
    }
}
```

The `data` attribute is a JSON object with zero or more attributes, each being the ID of the relevant data object as specified in the Data Query setup. Each of these objects will have a number of attributes depending on the fields chosen. Note that the names of these attributes **can** be overridden by the school. However, there is a unique numeric identifier that is appended to each which will remain constant. Logic should be based around that identifier. Note that custom fields will contain the word “custom” before the unique identifier and so that should also be checked for.

```
GET /api/dataquery/get/GXiE4V5qYB/2
```

Where the optional parameter “2” is included at the end, the structure of the returned data will change. An additional “fields” property is included with clearer textual descriptions of the fields. The fields in each of the data objects is identified by the immutable identifier. This allows automated systems to ignore parts of the field name that might change.

```json
{
    "fields": [
        {
           "id": 1,
           "name": "Admin Number"
        },
        {
           "id": 177,
           "name": "LURITS Number"
        },
        {
           "id": 6,
           "name": "Age"
        },
        {
           "id": 10,
           "name": "Gender"
        }  
    ],
    "data": {
        "49": {
            "1": "3316",
            "177": "",
            "6": "15 years, 200 days",
            "10": "Male"
        },
        "4688": {
            "1": "6333",
            "177": "",
            "6": "17 years, 10 days",
            "10": "Male"
        }
    },
    "message": "",
    "response": {
        "error": "OK",
        "code": 200
    }
}
```

### DataQuery/getsince:get

See above.

#### Request {#dataquerygetsinceget-request}

```
GET /api/dataquery/getsince/<secret>/<timestamp>[/<version>]
```

#### Parameters {#dataquerygetsinceget-parameters}

-   `<secret>` is the secret defined for a list. This also determines what type of data and which fields are returned.
-   `<timestamp>` is a [Unix integer timestamp](https://www.google.com/url?q=https://en.wikipedia.org/wiki/Unix_time&sa=D&source=editors&ust=1778246675689130&usg=AOvVaw3Bx1tu5NfQ41epG1AstACP).
-   `<version>` , if supplied, is the version of the data structure to be returned. See above.

#### Response {#dataquerygetsinceget-response}

See above.

### DataQuery/getone:get

See above.

#### Request {#dataquerygetoneget-request}

```
GET /api/dataquery/getone/<secret>/<identifier>[/<version>]
```

#### Parameters {#dataquerygetoneget-parameters}

-   `<secret>` is the secret defined for a list. This also determines what type of data and which fields are returned.
-   `<identifier>` is the identifier of the dataobject to be returned.
-   `<version>`, if supplied, is the version of the data structure to be returned. See above.

#### Response {#dataquerygetoneget-response}

See above.

### Documents/categories:get

Returns a list of document categories that the current API token has any permissions for, along with the permission flags for each.

#### Request {#documentscategoriesget-request}

```
GET /api/documents/categories
```

#### Parameters {#documentscategoriesget-parameters}

None.

#### Response {#documentscategoriesget-response}

The data attribute will be an array of zero or more JSON objects representing categories.

Example:

```
GET /api/documents/categories
```

```json
{
    "data": [
        {
            "category_id": 7,
            "category_name": "Photographs",
            "description": "Pupil photographs",
            "parent_id": 1,
            "permissions": {
                "read": true,
                "add": true,
                "delete": false
            }
        }
    ],
    "message": "",
    "response": {
        "error": "OK",
        "code": 200
    }
}
```

-   `category_id` is ADAM's internal identifier for the category.
-   `category_name` is the display name of the category.
-   `description**` is the category's description text.
-   `parent_id` is the identifier of the parent category (top-level categories have a parent of 0).
-   `permissions**` indicates which operations the token is allowed to perform on this category.

### Documents/list:get

Returns a list of documents for a given entity within a specific category.

#### Request {#documentslistget-request}

```
GET /api/documents/list/<categoryId>/<entityId>
```

#### Parameters {#documentslistget-parameters}

-   `categoryId`: The ADAM identifier of the document category.
-   `entityId`: The ADAM identifier of the entity (pupil, staff member, family, or site record).

#### Response {#documentslistget-response}

The data attribute will be an array of zero or more JSON objects representing documents. Requires **read** permission on the category.

Example:

```
GET /api/documents/list/108/4561
```

```json
{
    "data": [
        {
            "document_id": 12345,
            "name": "Birth Certificate",
            "filename": "birth_cert.pdf",
            "filetype": "application/pdf",
            "upload_date": "2025-03-15 10:30:00",
            "category_id": 108,
            "link": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
        }
    ],
    "message": "",
    "response": {
        "error": "OK",
        "code": 200
    }
}
```

-   `document_id` is ADAM's internal identifier for the document.
-   `name` is the descriptive name given to the document.
-   `filename` is the original filename of the uploaded file.
-   `filetype` is the MIME type of the document.
-   `upload_date` is the date and time the document was uploaded.
-   `category_id` is the category the document belongs to.
-   `link` is a unique random string identifier for the document.

### Documents/document:get

Returns detailed metadata for a single document, including its entity links.

#### Request {#documentsdocumentget-request}

```
GET /api/documents/document/<documentId>
```

#### Parameters {#documentsdocumentget-parameters}

-   `documentId`: The ADAM identifier of the document.

#### Response {#documentsdocumentget-response}

The data attribute will be a JSON object with document metadata and linked entities. Requires **read** permission on the document's category.

Example:

```
GET /api/documents/document/12345
```

```json
{
    "data": {
        "document_id": 12345,
        "name": "Birth Certificate",
        "notes": "",
        "filename": "birth_cert.pdf",
        "filetype": "application/pdf",
        "upload_date": "2025-03-15 10:30:00",
        "category_id": 108,
        "category_name": "Admin Documents",
        "link": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
        "links": [
            {
                "table": "pupils",
                "entity_id": 4561,
                "link_date": "2025-03-15 10:30:00"
            }
        ]
    },
    "message": "",
    "response": {
        "error": "OK",
        "code": 200
    }
}
```

- `notes` is any additional notes attached to the document.
- `category_name` is the display name of the document's category.
- `links` is an array of entity associations. Each link contains the entity `table` (pupils, staff, families, or site), the `entity_id`, and the `link_date`.

### Documents/download:get

Downloads the binary file content of a document.

#### Request {#documentsdownloadget-request}

```
GET /api/documents/download/<documentId>
```

#### Parameters {#documentsdownloadget-parameters}

- `documentId`: The ADAM identifier of the document.

#### Response {#documentsdownloadget-response}

Returns the raw binary file content with the appropriate Content-type header. Requires **read** permission on the document's category.

If the document is not found, a standard JSON error response is returned with code 404.

### Documents/upload:post

Uploads a new document and links it to an entity.

#### Request {#documentsuploadpost-request}

```
POST /api/documents/upload
```

The request body must be JSON with the following fields:

#### Parameters {#documentsuploadpost-parameters}

- `category` (required): The ADAM identifier of the target category.
- `entity_type` (required): The type of entity to link the document to. Must be one of: pupils, staff, families, site.
- `entity_id` (required): The ADAM identifier of the entity.
- `name` (required): A descriptive name for the document.
- `filename` (required): The filename (e.g. report.pdf).
- `file_data` (required): The file content encoded as a base64 string.
- `mimetype` (optional): The MIME type. If omitted, ADAM will attempt to detect it automatically.

#### Response {#documentsuploadpost-response}

Returns the new document's identifier. Requires **add** permission on the target category.

Example request body:

```json
{
  "category": 108,
  "entity_type": "pupils",
  "entity_id": 4561,
  "name": "Medical Certificate",
  "filename": "medical.pdf",
  "file_data": "JVBERi0xLjQK..."
}
```

Example response:

```json
{
  "data": {
    "document_id": 12346,
    "message": "Document uploaded successfully"
  },
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Documents/document:patch

Updates the metadata of an existing document. Can change the name, notes, or move the document to a different category.

#### Request {#documentsdocumentpatch-request}

```
PATCH /api/documents/document/<documentId>
```

The request body must be JSON with one or more of the following fields:

#### Parameters {#documentsdocumentpatch-parameters}

- `documentId` (URL): The ADAM identifier of the document.
- `name` (optional): New descriptive name for the document.
- `notes` (optional): New notes text for the document.
- `category` (optional): ADAM identifier of a category to move the document to. The token must also have **add** permission on the destination category.

#### Response {#documentsdocumentpatch-response}

Returns a success message. Requires **add** permission on the document's current category (and on the destination category if moving).

Example request body:

```json
{
  "name": "Updated Certificate",
  "notes": "Verified by admin"
}
```

Example response:

```json
{
  "data": {
    "message": "Document updated successfully"
  },
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Documents/document:delete

Permanently deletes a document and its file from the repository.

#### Request {#documentsdocumentdelete-request}

```
DELETE /api/documents/document/<documentId>
```

#### Parameters {#documentsdocumentdelete-parameters}

- `documentId`: The ADAM identifier of the document.

#### Response {#documentsdocumentdelete-response}

Returns a success message. Requires **delete** permission on the document's category.

Example:

```
DELETE /api/documents/document/12345
```

```json
{
  "data": {
    "message": "Document deleted successfully"
  },
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Export/families:get

Allows family information to be extracted easily.

#### Request {#exportfamiliesget-request}

```
GET /api/export/families
GET /api/export/families/all
GET /api/export/families/current
GET /api/export/families?updated_since=2024-10-01+08:15:30
GET /api/export/families/all?updated_since=2024-10-01+08:15:30
GET /api/export/families/current?updated_since=2024-10-01+08:15:30
```

#### Parameters {#exportfamiliesget-parameters}

The last parameter (all or current) may be omitted - the default setting is to return current families only. The structure of the data is unchanged.

An optional parameter, updated_since, will only return changes that have been made on or after the time specified. Any valid timestamp, that is URL encoded, can be used.

*Note well that changes to email addresses are* ***not*** *reflected in the modified time.*

#### Response {#exportfamiliesget-response}

Valid responses will contain an array of family objects in the data property. The family_primary_email and family_secondary_email will be arrays of email addresses:

```json
{
  "data": [
    {
      "family_id": 531,
      "family_admin": "0",
      "family_primary_lastname": "Adamson",
      "family_primary_firstname": "Adam",
      "family_primary_title": "Mr",
      "family_primary_idnum": "1234567890123",
      "family_primary_occupation": "Businessman",
      "family_primary_employer": "ADAM EduTech",
      "family_primary_workphone": "0615096077",
      "family_primary_cell": "0615096077",
      "family_secondary_lastname": "",
      "family_secondary_firstname": "",
      "family_secondary_idnum": "",
      "family_secondary_occupation": "",
      "family_secondary_employer": "",
      "family_secondary_workphone": "",
      "family_secondary_cell": "",
      "family_address_postal_1": "18 Lello Road",
      "family_address_postal_2": "",
      "family_address_postal_suburb": "Assagay",
      "family_address_postal_city": "Outer West Durban",
      "family_address_postal_province": "KwaZulu-Natal",
      "family_address_postal_code": "3600",
      "family_address_postal_country": "South Africa",
      "family_address_residential_1": "18 Lello Road",
      "family_address_residential_2": "",
      "family_address_residential_suburb": "Assagay",
      "family_address_residential_city": "Outer West Durban",
      "family_address_residential_province": "KwaZulu-Natal",
      "family_address_residential_code": "3610",
      "family_address_residential_country": "South Africa",
      "family_notes": "",
      "family_modify": "2024-09-18 08:37:41",
      "family_primary_email": [
        "testing+primary@testing.adam.co.za",
        "testing+primary2@testing.adam.co.za"
      ],
      "family_secondary_email": [
      ]
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### ExternalAuth/auth:post

Allows ADAM to be used as an external authentication source.

***Note well:*** *This API endpoint will divulge user information for a valid login name. As with any API key, it is imperative that it is kept secret and changed if a breach is suspected.*

#### Request {#externalauthauthpost-request}

```
POST /api/externalauth/auth/
```

#### Parameters {#externalauthauthpost-parameters}

These parameters are sent via form-data parameters.

- username: The username of the staff member or pupil, or the Identification number or passport number of a family member.
- password: The password associated with the username

#### Response {#externalauthauthpost-response}

Integrating systems should check the HTTP response code rather than the presence of user information in the data object.

If a valid username and password are supplied, the HTTP response code will be 200. The data object contains the user information and the contained response code will be 200:

```json
{
  "data": {
    "username": "admin",
    "firstname": "Patrick",
    "lastname": "Cloete",
    "email": "testing+staff_1@adam.co.za",
    "type": "staff",
    "id": "1"
  },
  "message": "",
  "response": {
    "error": "Login successful",
    "code": 200
  }
}
```

If a valid username is supplied, but the password is incorrect, the HTTP response code will be 401. The data object will contain user information and the contained response code will be 401:

```json
{
  "data": {
    "username": "admin",
    "firstname": "Patrick",
    "lastname": "Cloete",
    "email": "testing+staff_1@adam.co.za",
    "type": "staff",
    "id": "1"
  },
  "message": "",
  "response": {
    "error": "Username or password not recognised",
    "code": 401
  }
}
```

If an invalid username is supplied, the HTTP response code will be 401. The data object will be empty and the contained response code will be 401.

```json
{
  "data": [],
  "message": "",
  "response": {
    "error": "Username or password not recognised",
    "code": 401
  }
}
```

### Pupils/image:get

Returns an image of a pupil.

#### Request {#pupilsimageget-request}

```
GET /api/pupils/image/<pupil_id>
```

#### Parameters {#pupilsimageget-parameters}

- `<pupil_id>`: The internal identifier of the pupil.

#### Response {#pupilsimageget-response}

```
GET /api/reporting/pupils/image/123
```

Unlike other API calls, this will return an image file and not a JSON object. The image type will be specified by the response’s Content-Type header, but will almost certainly be a JPG image. A response code of 404 suggests that the image does not exist.

### Families/currentchildren:get

#### Request {#familiescurrentchildrenget-request}

```
GET /api/families/currentchildren/<family_id>
```

#### Parameters {#familiescurrentchildrenget-parameters}

- `<family_id>`: The internal identifier of the family.

#### Response {#familiescurrentchildrenget-response}

This query returns an array of pupils. If no pupils are attached to the family, or if the family identifier does not exist, then the response will be returned with a “404” HTTP status code.

```json
{
  "data": [
    "49",
    "4688"
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Famillies/email:get

Get a list of email addresses associated with a family or family member.

#### Request {#familliesemailget-request}

```
GET /api/families/email/<family_id>[/(primary|secondary)]
```

#### Parameters {#familliesemailget-parameters}

- `<family_id>`: The internal identifier of the family.
- (primary|secondary): OPTIONAL - whether to return only email addresses of the primary or secondary parent

#### Response {#familliesemailget-response}

This query returns an array of zero or more email address records.

```json
{
  "data": [
    {
      "email_id": 9372,
      "email_family_id": 123,
      "email_member": "primary",
      "email_address": "testing+245@test.adam.co.za",
      "email_description": "",
      "email_bulkmail": "Yes",
      "email_reports": "Yes",
      "email_alerts": "Yes",
      "email_maillog": "Yes",
      "email_modify": "2025-02-21 12:00:42"
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Families/email:post

Add an email address to a family member.

#### Request {#familiesemailpost-request}

```
POST /api/families/email/<family_id>/(primary|secondary)
```

#### Parameters {#familiesemailpost-parameters}

- `<family_id>`: The internal identifier of the family.
- (primary|secondary): Which parent the email address should be added to

In the POST body:

- email: a string containing the email address

#### Response {#familiesemailpost-response}

“201 Created” if added successfully, 200 if not added, with an appropriate error message in the response.error property (e.g. the email address may already exist?).

### Families/email:delete

Remove an email address to a family member.

#### Request {#familiesemaildelete-request}

```
DELETE /api/families/email/<family_id>/(primary|secondary)
```

#### Parameters {#familiesemaildelete-parameters}

- `<family_id>`: The internal identifier of the family.
- (primary|secondary): Which parent the email address should be added to

In the body which must be x-www-form-urlencoded:

- email: a string containing the email address to delete

#### Response {#familiesemaildelete-response}

200 if deleted successfully, 404 if not found, with an appropriate error message in the response.error property.

### Families/searchbyid:get

#### Request {#familiessearchbyidget-request}

```
GET /api/families/searchbyid/<RSA_ID_Number>
```

#### Parameters {#familiessearchbyidget-parameters}

- `<RSA_ID_Number>`: A South African ID number or international passport number for parents without an ID number. The parameter should be trimmed of spaces. This performs a simple text match with the database field and thus relies on reasonable data hygiene.

#### Response {#familiessearchbyidget-response}

This response returns an array of generally one family identifier, but if an ID number is associated with many parents, all will be returned in the array. This is discouraged in the interface, but schools may still do this.

Where the ID number cannot be found, a response will be returned with an HTTP 404 status code.

```json
{
  "data": [
    "1234"
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Families/children:get

Returns the children linked to a family. Alias: families/get_children_by_family.

#### Request {#familieschildrenget-request}

```
GET /api/families/children/<family>
```

#### Parameters {#familieschildrenget-parameters}

- `<family>`: ADAM internal family identifier (required)

#### Response {#familieschildrenget-response}

Data attribute contains an array of child records with pupil details, grade, and default class status.

```json
{
  "data": [
    {
      "pupil_id": 1234,
      "pupil_lastname": "Smith",
      "pupil_firstname": "John",
      "pupil_grade": "Grade 10",
      "pupil_defaultclass": "10A"
    }
  ]
}
```

Note: Pupils at the "pre" (admissions) stage show "Admission" instead of a class name, and will show their current grade rather than their grade of entry.

### Families/contactlist:get

Returns contact details for all families.

#### Request {#familiescontactlistget-request}

```
GET /api/families/contactlist
```

#### Parameters {#familiescontactlistget-parameters}

None.

#### Response {#familiescontactlistget-response}

```json
{
  "data": [
    {
      "id": 500,
      "primary": {
        "firstname": "Jane",
        "lastname": "Smith",
        "cell": "0821234567",
        "email": ["jane@example.com"]
      },
      "secondary": {
        "firstname": "John",
        "lastname": "Smith",
        "cell": "0829876543",
        "email": ["john@example.com"]
      }
    }
  ]
}
```

If no secondary contact exists, the secondary field is an empty array.

### Families/familyrelationships:get

Returns all pupil-to-family relationship mappings.

#### Request {#familiesfamilyrelationshipsget-request}

```
GET /api/families/familyrelationships
```

#### Parameters {#familiesfamilyrelationshipsget-parameters}

None.

#### Response {#familiesfamilyrelationshipsget-response}

```json
{
  "data": [
    { "pupil": 1234, "family": 500 },
    { "pupil": 1235, "family": 500 }
  ]
}
```

### Families/fields:get

Returns the list of valid fields for family records.

#### Request {#familiesfieldsget-request}

```
GET /api/families/fields/<action>
```

#### Parameters {#familiesfieldsget-parameters}

- `<action>`: Action context (optional; e.g. "add" or "edit" to filter relevant fields)

#### Response {#familiesfieldsget-response}

Data attribute contains a mapping of field names to their descriptions.

### Families/add:post

Creates a new family record.

#### Request {#familiesaddpost-request}

```
POST /api/families/add
```

#### Parameters {#familiesaddpost-parameters}

JSON request body containing family fields. Use families/fields to retrieve valid field names.

#### Response {#familiesaddpost-response}

- Code 200: Returns the new family ID
- Code 400: Validation error — response includes list of invalid fields

### Families/family:patch

Updates an existing family record.

#### Request {#familiesfamilypatch-request}

```
PATCH /api/families/family/<family>
```

#### Parameters {#familiesfamilypatch-parameters}

- `<family>`: ADAM internal family identifier (URL path parameter)
- JSON request body containing fields to update

#### Response {#familiesfamilypatch-response}

- Code 200: Returns the updated family record
- Code 400: Validation error
- Code 404: Family not found

### Families/link:post

Links a pupil to a family with specified relationship types.

#### Request {#familieslinkpost-request}

```
POST /api/families/link
```

#### Parameters {#familieslinkpost-parameters}

JSON request body:

```json
{
  "family_id": 500,
  "pupil_id": 1234,
  "primary_relationship": "biological",
  "secondary_relationship": "biological"
}
```

Valid relationship types: biological, adoptive parent, step parent, foster parent, guardian, sponsor, relative, other.

#### Response {#familieslinkpost-response}

Code 200 on success.

### Families/detailsupdateform:get

Triggers an email to the family with a details update form.

#### Request {#familiesdetailsupdateformget-request}

```
GET /api/families/detailsupdateform/<family>
```

#### Parameters {#familiesdetailsupdateformget-parameters}

- `<family>`: ADAM internal family identifier (required)

#### Response {#familiesdetailsupdateformget-response}

No data returned.

- Code 200: "Detail update form sent."
- Code 500: Error sending form

### FamilyLogin/privileges:get

Returns the portal privileges available for the currently authenticated family or pupil login.

#### Request {#familyloginprivilegesget-request}

```
GET /api/familylogin/privileges
```

#### Parameters {#familyloginprivilegesget-parameters}

None — uses the current authentication session context.

#### Response {#familyloginprivilegesget-response}

Data attribute maps pupil IDs to their available privilege strings.

```json
{
  "data": {
    "1234": ["marks", "reports", "absentee", "stats"],
    "1235": ["marks", "reports"]
  }
}
```

### FamilyRelationships/family:get

Gets a list of *current* pupils linked to a family with their relationships descriptors for primary and secondary parents.

#### Request {#familyrelationshipsfamilyget-request}

```
GET /api/familyrelationships/family[/<family_id>]
```

#### Parameters {#familyrelationshipsfamilyget-parameters}

- `<family_id>`: The internal identifier for the family. If omitted, all families are returned.

#### Response {#familyrelationshipsfamilyget-response}

The **data** attribute contains an array of 0 or more objects.

- The **index** of each array object is the identifier of the pupil.
- A **primary** and **secondary** key contain the relationship between the primary or secondary family member and the pupil. Note that a relationship will be returned even in instances where there may not be a secondary family member. Other logic must determine whether to discard this value or not.

Possible values include:

- biological
- adoptive parent
- stepparent
- foster parent
- guardian
- sponsor
- relative
- Other

```
GET /api/familyrelationships/family/123
```

```json
{
  "data": [
    {
      "111": {
        "primary": "biological",
        "secondary": "step parent"
      },
      "321": {
        "primary": "step parent",
        "secondary": "biological"
      }
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### FamilyRelationships/pupil:get

Gets a list of families linked to a pupil with their relationships descriptors for primary and secondary parents.

#### Request {#familyrelationshipspupilget-request}

```
GET /api/familyrelationships/pupil[/<pupil_id>]
```

#### Parameters {#familyrelationshipspupilget-parameters}

- `<pupil_id>`: The internal identifier for the pupil. If omitted, all pupils are returned

#### Response {#familyrelationshipspupilget-response}

```
GET /api/familyrelationships/pupil/123
```

```json
{
  "data": [
    "111": {
      "primary": "biological",
      "secondary": "step parent"
    },
    "321": {
      "primary": "step parent",
      "secondary": "biological"
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

The **data** attribute contains an array of 0 or more objects.

- The **index** of each array object is the identifier of the family.
- A **primary** and **secondary** key contain the relationship between the primary or secondary family member and the pupil. Note that a relationship will be returned even in instances where there may not be a secondary family member. Other logic must determine whether to discard this value or not.

Possible values include:

- biological
- adoptive parent
- step parent
- foster parent
- guardian
- sponsor
- relative
- Other

```
GET /api/familyrelationships/pupil
```

```json
{
  "data": [
    "123": {
      "111": {
        "primary": "biological",
        "secondary": "step parent"
      },
      "321": {
        "primary": "step parent",
        "secondary": "biological"
      }
    },
    "456": {
      "111": {
        "primary": "step parent",
        "secondary": "biological"
      }
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### FormFields/fields:get

Returns field definitions for a specified database table.

#### Request {#formfieldsfieldsget-request}

```
GET /api/formfields/fields/<table>/<action>
```

#### Parameters {#formfieldsfieldsget-parameters}

- `<table>`: Table name (required)
- `<action>`: Action context (optional)

#### Response {#formfieldsfieldsget-response}

Data attribute maps field names to their descriptions.

### Leaves/approved:get

Gets a list of approved leaves with an end date that is either today or in the future.

#### Request {#leavesapprovedget-request}

```
GET /api/leaves/approved[/<pupil>]
```

#### Parameters {#leavesapprovedget-parameters}

- `<pupil>`: Optional: The identifier of the pupil in question.

#### Response {#leavesapprovedget-response}

```
GET /api/leaves/approved/6050
```

```json
{
  "data": [
    {
      "leave_request_id": 4765,
      "leave_request_out": "2024-10-18 14:15:00",
      "leave_request_in": "2024-10-20 18:30:00",
      "leave_request_destination": "Home",
      "leave_request_host": "Parents",
      "leave_request_host_contact": "083",
      "leave_request_notes": "thanks",
      "leave_request_approval_notes": "\\n",
      "leave_request_status": "Approved",
      "leave_request_user_id": 1,
      "leave_request_user_type": "staff",
      "leave_request_submitted_datetime": "2024-10-15 10:37:01",
      "leave_request_reminder_datetime": null,
      "leave_request_choices": "Will he need Saturday Lunch:No\\nWill he need Sunday Supper:No\\nDo you need a gate code:No\\n",
      "leave_type_id": 1,
      "leave_type_description": "Full Weekend Leave",
      "leave_type_overnight": "Yes",
      "leave_type_off_campus": "Yes"
    }
  ],
  "message": "Leaves for Joseph Tshabalala",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

The **data** attribute contains an array of 0 or more leave records.

### Medical/offsport:get

Returns a list of pupil IDs currently off sport due to medical reasons.

#### Request {#medicaloffsportget-request}

```
GET /api/medical/offsport/<date>
```

#### Parameters {#medicaloffsportget-parameters}

- `<date>`: ISO-formatted date (optional; defaults to current date)

#### Response {#medicaloffsportget-response}

```json
{
  "data": [1234, 1567, 1890],
  "message": "Offsport list for 2026-04-09.",
  "response": { "error": "OK", "code": 200 }
}
```

### MessagingLogs/messages:get

Returns 20 delivered messages for a family or pupil, paginated.

#### Request {#messaginglogsmessagesget-request}

```
GET /api/messaginglogs/messages/<type>/<id>[/<start>]
```

#### Parameters {#messaginglogsmessagesget-parameters}

- `<type>`: family or pupil (required)
- `<id>`: Family or pupil identifier (required)
- `<start>`: Pagination offset (optional; defaults to 0). Returns 20 messages per page.

#### Response {#messaginglogsmessagesget-response}

Data attribute contains an array of delivered message summaries.

### MessagingLogs/message:get

Returns a single message's details.

#### Request {#messaginglogsmessageget-request}

```
GET /api/messaginglogs/message/<type>/<id>/<messageId>
```

#### Parameters {#messaginglogsmessageget-parameters}

- `<type>`: family, pupil, or staff (required)
- `<id>`: Identifier for the family, pupil, or staff member (required)
- `<messageId>`: Message identifier (required)

#### Response {#messaginglogsmessageget-response}

Data attribute contains the full message details.

### MessagingLogs/messagebyid:get

Returns a message by its ID, including attachments.

#### Request {#messaginglogsmessagebyidget-request}

```
GET /api/messaginglogs/messagebyid/<messageId>
```

#### Parameters {#messaginglogsmessagebyidget-parameters}

- `<messageId>`: Message identifier (required)

#### Response {#messaginglogsmessagebyidget-response}

Data attribute contains the message with an attachments array:

```json
{
  "data": {
    "message_id": 42,
    "subject": "Newsletter",
    "body": "...",
    "attachments": [
      { "link": "/path/to/file", "location": "docrep", "name": "Newsletter.pdf" }
    ]
  }
}
```

#### Privileges

Requires one of: messagelog_staff_view, messagelog_family_view, messagelog_pupil_view (staff tokens); or viewmessagelog_family, viewmessagelog_pupil (family/pupil tokens).

### Psychometric/assessmentsbycategory:get

Returns active psychometric assessments for a category. Alias: psychometric/assessments_by_category.

#### Request {#psychometricassessmentsbycategoryget-request}

```
GET /api/psychometric/assessmentsbycategory/<category>
```

#### Parameters {#psychometricassessmentsbycategoryget-parameters}

- `<category>`: Psychometric category identifier (required)

#### Response {#psychometricassessmentsbycategoryget-response}

Data attribute contains an array of active assessment records (where assessment_disabled = 'No').

### Pupils/add:post

#### Request {#pupilsaddpost-request}

```
POST /api/pupils/add
```

#### Parameters {#pupilsaddpost-parameters}

The body of the request is a JSON object of field names and values.

```json
{
  "pupil_id": 123,
  "pupil_lastname": "Adams",
  "pupil_firstname": "Adam",
  ...
}
```

#### Response {#pupilsaddpost-response}

The response code will determine whether the pupil was added or not, with invalid requests returning a 400 error. Acceptable field names can be inspected by using the [pupils/pupil:get](#pupilspupilget) endpoint. The following fields are mandatory:

- pupil_lastname - the pupil’s last name
- pupil_firstname - the pupil’s preferred legal name
- pupil_fullfirst - the pupil’s full names, excluding last name
- pupil_final - the pupil’s estimated Grade 12 year (NB - this must be the year of their Grade 12 year, even at a primary school level. ADAM uses this year to calculate the current grade a pupil is in)
- pupil_entry - the date when a pupil will enter the school. For pupils starting school at the start of an academic year, it is suggested to use is ‘year-01-01’ rather than the first day of term.

Note that while pupils may be added to the database even if these fields are omitted, doing so will make the pupils nearly impossible to manage on the receiving end.

For fields ending in an “_id” suffix, some values can be determined from [Appendix A](appendix-a-import-and-export-codes.md#appendix-a-import-and-export-codes). Note that pupil_registration_id field refers to a many-to-many relationship and thus cannot be completed by this end-point. If it exists in the submitted data, it is silently discarded.

If any other invalid fields are passed in, the response message will contain details of those invalid fields.

### Pupils/image:get {#api-resources-pupilsimageget}

#### Request {#api-resources-request}

```
GET /api/pupils/image/<ADAM_Identifier>[/<width>]
```

#### Parameters {#api-resources-parameters}

- `<ADAM_Identifier>`: An integer referring to the pupil’s internal ADAM identifier.
- `<width>`: An optional integer to determine the maximum width of the image. If omitted, the image is not resized. If the width provided is larger than the image’s width, the image will not be  resized.

#### Response {#api-resources-response}

This response returns an image. No JSON information is returned.

Where the identifier cannot be found, a response will be returned with an HTTP 404 status code.

### Pupils/pupil:get

#### Request {#pupilspupilget-request}

```
GET /api/pupils/pupil/<ADAM_Identifier>
```

#### Parameters {#pupilspupilget-parameters}

- `<ADAM_Identifier>`: An integer referring to the pupil’s internal ADAM identifier.

#### Response {#pupilspupilget-response}

This response returns a JSON object of data for a single pupil.

Where the identifier cannot be found, a response will be returned with an HTTP 404 status code.

```json
{
  "data": {
    "pupil_id": 123,
    "pupil_lastname": "Adams",
    "pupil_firstname": "Adam",
    ...
  },
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Pupils/search-admin:get

#### Request {#pupilssearch-adminget-request}

```
GET /api/pupils/search-admin/<AdminNumber>
```

#### Parameters {#pupilssearch-adminget-parameters}

- `<AdminNumber>`: The school-assigned administration number for a pupil.. The parameter should be trimmed of spaces. This performs a simple text match with the database field and thus relies on reasonable data hygiene.

#### Response {#pupilssearch-adminget-response}

This response returns an array of generally one pupil identifier, but if an Admin number is associated with many pupils, all will be returned in the array. This is discouraged in the interface, but schools may still do this.

Where the Admin number cannot be found, a response will be returned with an HTTP 404 status code.

```json
{
  "data": [
    "1234"
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Pupils/searchbyid:get

#### Request {#pupilssearchbyidget-request}

```
GET /api/pupils/search-id/<RSA_ID_Number>
GET /api/pupils/searchbyid/<RSA_ID_Number>
```

#### Parameters {#pupilssearchbyidget-parameters}

- `<RSA_ID_Number>`: A South African ID number or international passport number for pupils without an ID number. The parameter should be trimmed of spaces. This performs a simple text match with the database field and thus relies on reasonable data hygiene.

#### Response {#pupilssearchbyidget-response}

This response returns an array of generally one pupil identifier, but if an ID number is associated with many pupils, all will be returned in the array. This is discouraged in the interface, but schools may still do this.

Where the ID number cannot be found, a response will be returned with an HTTP 404 status code.

```json
{
  "data": [
    "1234"
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Pupils/fields:get

Returns the list of valid fields for pupil records.

#### Request {#pupilsfieldsget-request}

```
GET /api/pupils/fields/<action>
```

#### Parameters {#pupilsfieldsget-parameters}

- `<action>`: Action context (optional; e.g. "add" or "edit")

#### Response {#pupilsfieldsget-response}

Data attribute maps field names to their descriptions.

### Pupils/pupil:patch

Updates an existing pupil record.

#### Request {#pupilspupilpatch-request}

```
PATCH /api/pupils/pupil/<pupil>
```

#### Parameters {#pupilspupilpatch-parameters}

- `<pupil>`: ADAM internal pupil identifier (URL path parameter)
- JSON request body containing fields to update

#### Response {#pupilspupilpatch-response}

- Code 200: Returns the updated pupil record (includes pupil_gender as name and pupil_grade)
- Code 400: Validation error
- Code 404: Pupil not found

### Pupils/contactlist:get

Returns contact details for all pupils.

#### Request {#pupilscontactlistget-request}

```
GET /api/pupils/contactlist
```

#### Parameters {#pupilscontactlistget-parameters}

None.

#### Response {#pupilscontactlistget-response}

```json
{
  "data": [
    {
      "id": 1234,
      "firstname": "John",
      "lastname": "Smith",
      "cell": "0821234567",
      "email": "john@example.com",
      "grade": "Grade 10"
    }
  ]
}
```

### Pupils/search-id:get

Searches for pupils by ID number. Alias: pupils/searchbyid (note: this is a different endpoint from the documented Pupils/searchbyid which searches by admin number — verify the documented version is correct).

#### Request {#pupilssearch-idget-request}

```
GET /api/pupils/search-id/<idNumber>
```

#### Parameters {#pupilssearch-idget-parameters}

- `<idNumber>`: ID number to search for (required)

#### Response {#pupilssearch-idget-response}

- Code 200: Array of matching pupil IDs
- Code 400: Empty idNumber parameter
- Code 404: No pupils found

### RecordsAndPoints/recentpupilrecords:get

Returns the most recent Records and Points entries for a pupil.

#### Request {#recordsandpointsrecentpupilrecordsget-request}

```
GET /api/recordsandpoints/recentpupilrecords/<pupil>[/<number>]
```

#### Parameters {#recordsandpointsrecentpupilrecordsget-parameters}

- `<pupil>`: ADAM internal pupil identifier (required)
- `<number>`: Maximum number of records to return (optional; defaults to 10)

#### Response {#recordsandpointsrecentpupilrecordsget-response}

```json
{
  "data": [
    {
      "group_name": "Bad",
      "category_description": "Demerit",
      "discipline_date": "2026-04-01 08:30:00",
      "discipline_effective_date": "2026-04-01",
      "discipline_amount": 1,
      "discipline_notes": "Late to class",
      "option_description": null
    }
  ]
}
```

### RecordsAndPoints/pupilrecords:get

Returns all Records and Points entries for a pupil, grouped by category group and category.

#### Request {#recordsandpointspupilrecordsget-request}

```
GET /api/recordsandpoints/pupilrecords/<pupil>
```

#### Parameters {#recordsandpointspupilrecordsget-parameters}

- `<pupil>`: ADAM internal pupil identifier (required)

#### Response {#recordsandpointspupilrecordsget-response}

Data attribute is a nested structure grouped by discipline group, then by category, with all records within each category.

```json
{
  "data": {
    "1": {
      "group_name": "Bad",
      "discipline_categories": [
        {
          "category_description": "Demerit",
          "discipline_records": [
            {
              "discipline_date": "2026-04-01",
              "discipline_amount": 1,
              "discipline_notes": "Late to class"
            }
          ]
        }
      ]
    }
  }
}
```

### Registration/status:post

Updates the registration status of a pupil by adding a record to their registration status log.

#### Request {#registrationstatuspost-request}

```
POST /api/registration/status/<pupil>
```

#### Parameters {#registrationstatuspost-parameters}

URL parameters:

- `<pupil>`: The identifier of the pupil whose registration status is to be changed.

These parameters are sent via form-data parameters.

- status: The identifier of the new registration status
- notes: Notes to add to the registration status

#### Response {#registrationstatuspost-response}

If the request was successful, a 200 OK code is returned. If an invalid status was chosen, a 400 Bad Request code is returned.

This endpoint is restricted in that updating the registration status of a pupil cannot change the “stage” of a pupil’s registration (a “stage” being one of “admissions”, “current enrolment” or “alumni”). Changing to a new stage requires additional processing to be done within ADAM and so attempts to change between statuses that are from different stages will be responded to with a 400 code.

### Registration/statuses:get

Gets a list of registration statuses that are active on the system.

#### Request {#registrationstatusesget-request}

```
GET /api/registration/statuses
```

#### Parameters {#registrationstatusesget-parameters}

None

#### Response {#registrationstatusesget-response}

```
GET /api/registration/statuses
```

```json
{
  "data": [
    {
      "status_id": 1,
      "status_description": "Applicant",
      "status_stage": "pre",
      "status_active": "Yes",
      "status_default": "Yes",
      "status_official": "Yes",
      "status_familyshow": "Yes",
      "status_sortorder": 1
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

- status_stage is an enum with values pre (pre-admission), current (pupils enrolled in the school) or post (alumni and graduated pupils).

The following boolean values are also given:

- status_active: Whether the pupil record is active or inactive. Inactive pupils might include those who have withdrawn from the registration process, withdrawn from the school, died, and so on. When combined with status_stage, this provides [six broad categories of registration status](enrolment-process.md#enrolment-process).
- status_default: Each of the three status_stage values has one default status. This is automatically applied to pupils entering this stage for the first time.
- status_official: Whether this status refers to an official enrolment or not. Unofficial enrolments may include exchange or visiting pupils.
- status_familyshow: Whether or not pupils with this status should be shown on the family portal. For example, it can be distressing for parents of a deceased child to see that child appear on their family portal landing page. Similarly, withdrawn pupils might not show, but graduated pupils should.

### Registration/statuslist:get

Gets a list of pupils who belong to a specific registration status

#### Request {#registrationstatuslistget-request}

```
GET /api/registration/statuslist/<status>
```

#### Parameters {#registrationstatuslistget-parameters}

- `<status>`: The identifier of the registration status.

#### Response {#registrationstatuslistget-response}

```
GET /api/registration/statuslist/2
```

```json
{
  "data": [
    1,
    123,
    4321
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

The data attribute contains an array of 0 or more integers representing the identifiers of pupils who belong to this registration status.

### Registrations/grade:get

Returns a list of classes that a grade of pupils is registered for.

#### Request {#registrationsgradeget-request}

```
GET /api/registrations/grade/<grade>
```

#### Parameters {#registrationsgradeget-parameters}

- `<grade>` is an integer representing the grade of pupils to retrieve from the database. Note that 0 represents Grade R and negative grades represent the pre-school grades.

#### Response {#registrationsgradeget-response}

The response is an array of pupil registration objects, each following the structure below:

```json
{
  "data": [
    {
      "registration_id": 162555,
      "pupil_id": 1234,
      "pupil_lastname": "Last-Name",
      "pupil_firstname": "First",
      "class_id": 4231,
      "class_description": "Z",
      "class_gradeyear": "11",
      "subject_id": 101,
      "subject_name": "English Home Language",
      "subject_short": "Eng",
      "category_id": 1,
      "category_description": "Academic",
      "registration_datestart": "2024-01-20",
      "registration_dateend": null,
      "staff_id": 123,
      "staff_firstname": "Educator",
      "staff_lastname": "Mary"
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Reporting/periods:get

Gets a list of reporting periods for a year.

#### Request {#reportingperiodsget-request}

```
GET /api/reporting/periods[/<year>]
```

#### Parameters {#reportingperiodsget-parameters}

- `<year>`: OPTIONAL. The calendar year in question. If omitted, the current calendar year is used.

#### Response {#reportingperiodsget-response}

```
GET /api/reporting/periods/2018
```

```json
{
  "data": [
    {
      "period_id": "31",
      "period_name": "Term 1",
      "period_start": "2018-01-01",
      "period_end": "2018-12-02",
      "period_publish": "2018-12-02 12:00:00"
    }
  ],
  "message": "Reporting periods from year 2018",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

The **data** attribute contains an array of 0 or more reporting period objects.

- `period_id` is the internal identifier for the reporting period in question.
- `period_name` is the user-provided descriptor for that reporting period.
- `period_start` is the starting date of the reporting period. This is often set as the start of term, but some schools, who run concurrent or additional reporting periods may not align reporting periods with terms.
- `period_end` is the date on which the reporting period is deemed to have finished.
- `period_publish` is the date and time when the reports are made available on the parent portal. This date may change at the user discretion and so this value should always be double checked on or after this time if important actions are to occur.

### Reporting/results:get

Gets all academic results for a reporting period.

#### Request {#reportingresultsget-request}

```
GET /api/reporting/results/<reportingperiod>
```

#### Parameters {#reportingresultsget-parameters}

- `<reportingperiod>` is the value of the reporting period identifier. See the `period_id` property returned in the Reporting/periods/get request above.

#### Response {#reportingresultsget-response}

```
GET /api/reporting/results/31
```

```json
{
  "data": [
    {
      "pupil_id": 1754,
      "pupil_admin": "55012",
      "pupil_grade": 9,
      "results": [
        {
          "subject_id": 1,
          "subject_name": "English",
          "dbe_subject_code": "",
          "result_term": 50,
          "result_ytd": 50
        },
        {
          "subject_id": 40,
          "subject_name": "Technology",
          "dbe_subject_code": "15351142",
          "result_term": null,
          "result_ytd": null
        }
      ],
      "report_aggregate": 72.5,
      "report_aggregate_ytd": 72.5,
      "report_modified": "2016-02-11 11:36:17"
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

The **data** attribute contains an array of 0 or more pupil objects. The pupil object has the following attributes:

- `pupil_id` the internal identifier of the pupil.
- `pupil_admin` is a user-provided identifier. These should be consistent but can change at the school’s discretion.
- `pupil_grade` gives the grade that the pupil was in for this reporting period. Values are integers between -3 (Grade 0000) and 13 (Post Matric).
- **results** is an array of 0 or more subject result objects. These objects have the following properties:

- `subject_id` is the internal identifier for the subject in ADAM. Note that these may not be consistent as some schools have multiple versions of the same subject (e.g. English for Junior School vs English for High School). These values are not consistent across schools.
- `subject_name` is the user-provided name for that subject.
- `dbe_subject_code` is the Department of Basic Education’s subject code. Typically, this is specific to the grade and subject. Because some schools offer their curriculum in different configurations, some codes may be duplicated, and yet other subjects may not have a code assigned (which is represented by an empty string).
- `result_term` is the pupil’s result for this reporting period (normally akin to a term). A **null** value represents an absent result. This result is otherwise returned as a **float** and decimal places should be anticipated
- `result_ytd` is the pupil’s year-to-date result, a result that is often an aggregated result across a number of reporting periods. A **null** value represents an absent result.This result is otherwise returned as a **float** and decimal places should be anticipated.

- `report_aggregate` is a summary result (often, but not always, an average of all the subject results) for the pupil for that term.
- `report_aggregate_ytd` is a summary year-to-date result. Again, this is often, but not always an average of the subject results.
- `report_modified` is a timestamp of the last modification time of that report.

### Reporting/pupilreportingperiods:ge

Returns reporting periods available for a specific pupil, including report availability.

#### Request {#reportingpupilreportingperiodsge-request}

```
GET /api/reporting/pupilreportingperiods/<pupil>
```

#### Parameters {#reportingpupilreportingperiodsge-parameters}

- `<pupil>`: ADAM internal pupil identifier (required)

#### Response {#reportingpupilreportingperiodsge-response}

```json
{
  "data": [
    {
      "period_id": 3,
      "period_name": "Term 1 2026",
      "period_start": "2026-01-15",
      "period_end": "2026-03-31",
      "period_publish": "Yes",
      "report_aggregate": 72.5,
      "report_aggregate_ytd": 72.5,
      "document_id": 456,
      "document_upload_date": "2026-04-01",
      "pupil_gradetext": "Grade 10"
    }
  ]
}
```

### Reporting/subjectmarksbypupil:get

Returns subject marks for a pupil across all reporting periods.

#### Request {#reportingsubjectmarksbypupilget-request}

```
GET /api/reporting/subjectmarksbypupil/<pupil>
```

#### Parameters {#reportingsubjectmarksbypupilget-parameters}

- `<pupil>`: ADAM internal pupil identifier (required)

#### Response {#reportingsubjectmarksbypupilget-response}

Data attribute contains an array of reporting periods, each with a nested subjects array:

```json
{
  "data": [
    {
      "period_id": 3,
      "period_name": "Term 1 2026",
      "subjects": [
        {
          "subject_id": 5,
          "grade": 10,
          "subject_name": "Mathematics",
          "subject_short": "Maths",
          "teacher_email": "smith@school.co.za",
          "teacher_name": "Mr Smith",
          "result": 78,
          "class_friendly": "10A Maths"
        }
      ]
    }
  ]
}
```

### Reporting/markbook:get

Returns the markbook (assessment results by category) for a pupil in a specific reporting period.

#### Request {#reportingmarkbookget-request}

```
GET /api/reporting/markbook/<period>/<pupil>
```

#### Parameters {#reportingmarkbookget-parameters}

- `<period>`: Reporting period identifier (required)
- `<pupil>`: ADAM internal pupil identifier (required)

#### Response {#reportingmarkbookget-response}

Data attribute contains an array of subjects with assessment categories and individual assessments.

```json
{
  "data": [
    {
      "subject_name": "Mathematics",
      "subject_short": "Maths",
      "class_teacher": "Mr Smith",
      "class_gradeyear": 10,
      "class_description": "10A",
      "class_friendly": "10A Maths",
      "assessment_categories": [
        {
          "category_name": "Tests",
          "assessments": []
        }
      ]
    }
  ]
}
```

### Reporting/report:get

Returns a pupil's report as a PDF document.

#### Request {#reportingreportget-request}

```
GET /api/reporting/report/<period>/<pupil>
```

#### Parameters {#reportingreportget-parameters}

- `<period>`: Reporting period identifier (required)
- `<pupil>`: ADAM internal pupil identifier (required)

#### Response {#reportingreportget-response}

Binary PDF response with content type application/pdf.

### Reporting/previousreports:get

Returns historical report information for a pupil.

#### Request {#reportingpreviousreportsget-request}

```
GET /api/reporting/previousreports/<pupil>
```

#### Parameters {#reportingpreviousreportsget-parameters}

- `<pupil>`: ADAM internal pupil identifier (required)

#### Response {#reportingpreviousreportsget-response}

Data attribute contains previous report table data.

### Request/test:get

A test method to the API.

#### Request {#requesttestget-request}

```
GET /api/request/test/[Parameter1]/[Parameter2]
```

#### Parameters {#requesttestget-parameters}

[Parameter1]: An arbitrary parameter that is returned.

[Parameter2]: An arbitrary parameter that is returned.

#### Output

The output data will be a JSON object containing attributes parameter1 and parameter2, both of which will contain the values provided in the request.

**Example:**

```
https://demo.adam.co.za/api/request/test/First%20Parameter/Second
```

```json
{
  "data": {
    "parameter1": "First Parameter",
    "parameter2": "Second"
  },
  "message": "Hello, you're speaking to Random High School's ADAM. We are currently on revision 6125 and the local time is 11:26:46.",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

### Staff/image:get

Returns an image of a staff member.

#### Request {#staffimageget-request}

```
GET /api/staff/image/<staff_id>
```

#### Parameters {#staffimageget-parameters}

- `<staff_id>`: The internal identifier of the pupil.

#### Response {#staffimageget-response}

```
GET /api/reporting/staff/image/123
```

Unlike other API calls, this will return an image file and not a JSON object. The image type will be specified by the response’s Content-Type header, but will almost certainly be a JPG image. A response code of 404 suggests that the image does not exist.

### Subjects/get_by_grades:get

Returns subjects available for one or more grades.

#### Request {#subjectsgetbygradesget-request}

```
GET /api/subjects/get_by_grades/<grades>
```

#### Parameters {#subjectsgetbygradesget-parameters}

- `<grades>`: Comma-separated list of grade identifiers (required)

#### Response {#subjectsgetbygradesget-response}

Data attribute contains an array of subjects valid for the specified grades that have active class registrations.

### Subjects/get_by_grade:get

Returns subjects available for a single grade.

#### Request {#subjectsgetbygradeget-request}

```
GET /api/subjects/get_by_grade/<grade>
```

#### Parameters {#subjectsgetbygradeget-parameters}

- `<grade>`: Grade identifier (required)

#### Response {#subjectsgetbygradeget-response}

Data attribute contains an array of subjects for the specified grade with active class registrations.

### TableFields/fields:get

Returns field definitions for a specified database table. Similar to FormFields/fields but uses the TableFields system.

#### Request {#tablefieldsfieldsget-request}

```
GET /api/tablefields/fields/<table>/<action>
```

#### Parameters {#tablefieldsfieldsget-parameters}

- `<table>`: Table name (required)
- `<action>`: Action context (optional)

#### Response {#tablefieldsfieldsget-response}

Data attribute maps field names to their descriptions.

### XDevMan/alumni:get

Returns a list of Alumni and their last-modified dates

#### Request {#xdevmanalumniget-request}

```
GET /api/xdevman/alumni/<year>
```

#### Parameters {#xdevmanalumniget-parameters}

- `<year>`: The year of matriculation of the pupils

#### Response {#xdevmanalumniget-response}

```
GET /api/xdevman/alumni/2019
```

```json
{
  "data": [
    {
      "pupil_id": "2240",
      "pupil_admin": "7623",
      "pupil_modify": "2019-11-11 16:25:54",
      "alumni_modify": "2020-01-02 16:04:04"
    },
    {
      "pupil_id": "1319",
      "pupil_admin": "7289",
      "pupil_modify": "2019-11-11 16:25:54",
      "alumni_modify": "2020-01-02 16:04:04"
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

In each record, the internal ID and school-provided administration number are returned. There are two modification times because data for alumni is stored in two separate places (one from the historical pupil information, and another from the alumni-specific information).

### XDevMan/currentpupils:get

Returns a list of current pupils and their list of modification dates.

#### Request {#xdevmancurrentpupilsget-request}

```
GET /api/xdevman/currentpupils
```

#### Parameters {#xdevmancurrentpupilsget-parameters}

- none

#### Response {#xdevmancurrentpupilsget-response}

```
GET /api/xdevman/currentpupils
```

```json
{
  "data": [
    {
      "pupil_id": "2240",
      "pupil_admin": "7623",
      "pupil_modify": "2019-11-11 16:25:54"
    },
    {
      "pupil_id": "1319",
      "pupil_admin": "7289",
      "pupil_modify": "2019-11-11 16:25:54"
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

In each record, the internal ID and school-provided administration number are returned. There are two modification times because data for alumni is stored in two separate places (one from the historical pupil information, and another from the alumni-specific information).

### XDevMan/leavers:get

Returns a list of Leavers and their last-modified dates. A leaver for a year is a person who was deregistered during the course of that year. It includes people from all grades.

#### Request {#xdevmanleaversget-request}

```
GET /api/xdevman/leavers/<year>
```

#### Parameters {#xdevmanleaversget-parameters}

- `<year>`: The year of matriculation of the pupils

#### Response {#xdevmanleaversget-response}

```
GET /api/xdevman/leavers/2019
```

```json
{
  "data": [
    {
      "pupil_id": "2240",
      "pupil_admin": "7623",
      "pupil_modify": "2019-11-11 16:25:54",
      "alumni_modify": "2020-01-02 16:04:04"
    },
    {
      "pupil_id": "1319",
      "pupil_admin": "7289",
      "pupil_modify": "2019-11-11 16:25:54",
      "alumni_modify": "2020-01-02 16:04:04"
    }
  ],
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

In each record, the internal ID and school-provided administration number are returned. There are two modification times because data for alumni is stored in two separate places (one from the historical pupil information, and another from the alumni-specific information).

### XDevMan/alumnus:get

Returns the details of a single alumnus.

#### Request {#xdevmanalumnusget-request}

```
GET /api/xdevman/alumnus/<pupil_id>
```

#### Parameters {#xdevmanalumnusget-parameters}

- `<year>`: The year of matriculation of the pupils

#### Response {#xdevmanalumnusget-response}

```
GET /api/xdevman/alumnus/999
```

```json
{
  "data": {
    "pupil_id": "999",
    "pupil_admin": "6727",
    "pupil_lastname": "xxx",
    "pupil_firstname": "xxx",
    "pupil_fullfirst": "xxx",
    "pupil_birth": "1994-08-xx",
    "pupil_final": "2012",
    "pupil_gender": "Female",
    "pupil_entry": "2010-07-12",
    "pupil_exit": "2012-12-31",
    "pupil_idnumber": "9408xxx",
    "pupil_population_id": "4",
    "pupil_language_id": "2",
    "pupil_language_other": "",
    "pupil_email": "",
    "pupil_email_personal": "",
    "pupil_prepschool": "xxx",
    "pupil_nationality": "South Africa",
    "pupil_boarder": "3",
    "alumni_title": "Miss",
    "alumni_marital_status": "",
    "alumni_maiden_name": "",
    "alumni_spouse_title": "",
    "alumni_spouse_firstname": "",
    "alumni_spouse_gender": null,
    "alumni_spouse_occupation": "",
    "alumni_date_married": "0000-00-00",
    "alumni_region": "",
    "alumni_district": "",
    "alumni_branch_id": null,
    "alumni_type_id": "1",
    "alumni_deceased": "No",
    "alumni_deceased_date": null,
    "alumni_workphone": "",
    "alumni_homephone": "(031) xxx 6xxx",
    "alumni_other": "",
    "alumni_reason_left": "",
    "alumni_exit_grade": "12",
    "alumni_previous_school": null,
    "alumni_qualification": "Senior Certificate",
    "family": {
      "families": [
        {
          "family_id": "873",
          "family_admin": "0",
          "family_primary_lastname": "xxx",
          "family_primary_firstname": "xxx",
          "family_primary_fullfirst": "xxx",
          "family_primary_initials": "X",
          "family_primary_title": "Mr",
          "family_primary_idnum": "651xxxx",
          "family_primary_gender": "Male",
          "family_primary_occupation": "xxx",
          "family_primary_employer": "xxx",
          "family_primary_workphone": "0315xxx",
          "family_primary_cell": "083xxx",
          "family_primary_birth": "1965-10-xx",
          "family_secondary_lastname": "xxx",
          "family_secondary_firstname": "xxx",
          "family_secondary_fullfirst": "xxx",
          "family_secondary_initials": "X",
          "family_secondary_title": "Mrs",
          "family_secondary_idnum": "6607xxx",
          "family_secondary_gender": "Female",
          "family_secondary_occupation": "xxx",
          "family_secondary_employer": "xxx",
          "family_secondary_workphone": "0315xxx",
          "family_secondary_cell": "083xxx",
          "family_secondary_birth": "1966-07-xx",
          "family_address_postal_1": "xxx",
          "family_address_postal_2": "xxx",
          "family_address_postal_suburb": "xxx",
          "family_address_postal_city": "",
          "family_address_postal_province": "",
          "family_address_postal_code": "xxx",
          "family_address_postal_country": "South Africa",
          "family_address_residential_1": "xxx",
          "family_address_residential_2": "xxx",
          "family_address_residential_suburb": "xxx",
          "family_address_residential_city": "",
          "family_address_residential_province": "",
          "family_address_residential_code": "",
          "family_address_residential_country": "xxx",
          "family_home_phone": "03150xxx",
          "family_home_fax": "03150xxx"
        }
      ],
      "email": [
        {
          "email_family_id": "873",
          "email_member": "primary",
          "email_address": "xxx@example.com"
        },
        {
          "email_family_id": "873",
          "email_member": "secondary",
          "email_address": "yyy@example.com"
        }
      ]
    }
  },
  "message": "",
  "response": {
    "error": "OK",
    "code": 200
  }
}
```

A record of a single alumnus is returned.

## Specific Integration Requirements

Please see the [Third Party Integration](third-party-integration.md#third-party-integration) section in this documentation.
