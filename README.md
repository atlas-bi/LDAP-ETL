# Atlas Supplementary LDAP ETL

## What it does

This supplementary ETL loads data from an LDAP server into a database that is accessable by the primary [Atlas metadata ETL](https://github.com/atlas-bi/atlas-bi-libaray-etl).


## Setup

Create a `settings.py` file with the following settings, modified to fit your needs.

```py
server_uri = "ldap.example.net"
username = "MYORG\\my_user"
password = "my_pass"
database = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=server_name;DATABASE=LDAP;UID=user_name;PWD=password"
ad_domain = "MYORG"
dc = "MyOrg"
search_bases = ["EPIC", "Employees", "Doctors", "Non-Staff", "Students", "Volunteers"]

group_search_bases = [
    "Email Distribution Groups",
    "Room & Shared Mailboxes",
    "Access & Permissions",
]
```

## Other Tools

[Active Directory Explorer](https://docs.microsoft.com/en-us/sysinternals/downloads/adexplorer) is a useful tool to browse your LDAP setup to find the correct bases and dc.
