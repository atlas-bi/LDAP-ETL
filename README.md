<h1 align="center">LDAP ETL</h1>
<h4 align="center">Atlas BI Library ETL | LDAP Supplimentary ETL</h4>
<p align="center">
 <a href="https://www.atlas.bi" target="_blank">Website</a> • <a href="https://demo.atlas.bi" target="_blank">Demo</a> • <a href="https://www.atlas.bi/docs/bi-library/" target="_blank">Documentation</a> • <a href="https://discord.gg/hdz2cpygQD" target="_blank">Chat</a>
</p>
<p align="center">
<a href="https://www.codacy.com/gh/atlas-bi/LDAP-ETL/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=atlas-bi/LDAP-ETL&amp;utm_campaign=Badge_Grade"><img alt="codacy" src="https://app.codacy.com/project/badge/Grade/0bf456a89c4444709d5d9897722f6181"></a>
 <a href="https://sonarcloud.io/project/overview?id=atlas-bi_LDAP-ETL"><img alt="maintainability" src="https://sonarcloud.io/api/project_badges/measure?project=atlas-bi_LDAP-ETL&metric=sqale_rating"></a>
 <a href="https://discord.gg/hdz2cpygQD"><img alt="discord chat" src="https://badgen.net/discord/online-members/hdz2cpygQD/" /></a>
 <a href="https://github.com/atlas-bi/LDAP-ETL/releases"><img alt="latest release" src="https://badgen.net/github/release/atlas-bi/LDAP-ETL" /></a>

<p align="center">Loads data from an LDAP server into a database that is accessible by the primary <a href="https://github.com/atlas-bi/atlas-bi-libaray-etl">Atlas metadata ETL</a>.
 </p>


## 🏃 Getting Started

### Create Database

Use the [`LDAPDatabaseCreationScript.sql`](https://raw.githubusercontent.com/atlas-bi/LDAP-ETL/master/LDAPDatabaseCreationScript.sql) to create a database with the required tables.

### Install Packages

`poetry install`


### Create `.env` file

Create a `.env` file with the following settings, modified to fit your needs.

(or, pass the variables as environment variables)

```env
SERVERURI=ldap.example.com
ADUSERNAME=EXAMPLEHEALTH\me
ADPASSWORD=exampl3
DATABASE=DRIVER={ODBC Driver 17 for SQL Server};SERVER=atlas;DATABASE=LDAP;UID=datagov;PWD=123
ADDOMAIN=EXAMPLEHEALTH
DC=ExampleHealth
SEARCHBASES=EPIC, Employees, Doctors, Non-Staff, Students, Volunteers
GROUPSEARCHBASES=Email Distribution Groups, Room & Shared Mailboxes,Access & Permissions
```

### Running

`poetry run python ldap.py`

## Other Tools

[Active Directory Explorer](https://docs.microsoft.com/en-us/sysinternals/downloads/adexplorer) is a useful tool to browse your LDAP setup to find the correct bases and dc.
