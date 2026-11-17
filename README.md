<h1 align="center">LDAP ETL</h1>
<h4 align="center">Atlas BI Library ETL | LDAP Supplementary ETL</h4>
<p align="center">
  <a href="https://www.atlas.bi" target="_blank">Website</a> •
  <a href="https://demo.atlas.bi" target="_blank">Demo</a> •
  <a href="https://www.atlas.bi/docs/library/" target="_blank">Documentation</a> •
  <a href="https://discord.gg/hdz2cpygQD" target="_blank">Chat</a>
</p>

<p align="center">
  Loads data from an LDAP server into a database accessible by the primary
  <a href="https://github.com/atlas-bi/atlas-bi-library-etl">Atlas metadata ETL</a>.
</p>

## Getting started

### Create database

Use [`LDAPDatabaseCreationScript.sql`](LDAPDatabaseCreationScript.sql) to create the required tables.

### System dependencies

- [Python](https://www.python.org/downloads/) 3.10+
- [uv](https://docs.astral.sh/uv/)
- [C++ build tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) on Windows
- [ODBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### Install packages

```bash
uv sync
```

### Create `.env` file

Create a `.env` file (or pass the same values as environment variables):

```env
LDAP_HOST=localhost
LDAP_USERNAME=cn=admin,dc=example,dc=org
LDAP_PASSWORD=adminpassword
LDAP_BASE=dc=example,dc=org
LDAP_USE_SSL=False
LDAP_USE_TLS=False

AD_DOMAIN=EXAMPLEHEALTH

LDAP_GROUP_SEARCH=(objectClass=group)

# Optionally limit results to DNs that contain an OU (comma-separated).
LDAP_GROUP_OU=Email Distribution Groups,Room & Shared Mailboxes,Access & Permissions

LDAP_GROUP_USERNAME=sAMAccountName
LDAP_GROUP_DISPLAYNAME=displayName
LDAP_GROUP_EMAIL=mail,email

LDAP_USER_SEARCH=(&(objectClass=person)(sAMAccountName=*))
LDAP_USER_EMPLOYEEID=employeeID
LDAP_USER_ACCOUNTNAME=sAMAccountName
LDAP_USER_DISPLAYNAME=displayName
LDAP_USER_FULLNAME=cn,name
LDAP_USER_FIRSTNAME=givenName
LDAP_USER_LASTNAME=sn
LDAP_USER_DEPARTMENT=department
LDAP_USER_TITLE=title,description
LDAP_USER_PHONE=ipPhone,telephoneNumber
LDAP_USER_EMAIL=mail,proxyAddresses,userPrincipalName
LDAP_USER_PHOTO=thumbnailPhoto,profilePhoto

DATABASE=DRIVER={ODBC Driver 17 for SQL Server};SERVER=atlas;DATABASE=LDAP;UID=datagov;PWD=123
```

### Running

```bash
uv run python ldap.py
```

## Other tools

[Active Directory Explorer](https://docs.microsoft.com/en-us/sysinternals/downloads/adexplorer) is useful for browsing LDAP to find bases and DCs.

## Testing

1. Start an LDAP server:

```bash
docker run -p 389:1389 bitnami/openldap:latest
```

2. Set test env vars:

```env
LDAP_HOST=ldap://localhost:389
LDAP_USERNAME=cn=admin,dc=example,dc=org
LDAP_PASSWORD=adminpassword
DATABASE=>> your test db connection
AD_DOMAIN=
LDAP_BASE=dc=example,dc=org
LDAP_USER_SEARCH=(objectClass=inetOrgPerson)
LDAP_GROUP_SEARCH=(objectClass=groupOfNames)
LDAP_USE_SSL=false
LDAP_USE_TLS=false
```

3. Run tests:

```bash
uv sync --group dev
uv run pytest tests.py
```
