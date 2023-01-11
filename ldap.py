"""Atlas Supplementary LDAP ETL."""
import os
import re
from typing import Dict, List, Union

import pyodbc
from dotenv import load_dotenv
from ldap3 import ALL, SUBTREE, Connection, Server

load_dotenv()

SERVERURI = os.environ.get("SERVERURI", "ldap.example.com")
PASSWORD = os.environ.get("ADPASSWORD", "exampl3")

USERNAME = os.environ.get("ADUSERNAME", "me")

DATABASE = os.environ.get(
    "DATABASE",
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=atlas;DATABASE=LDAP;UID=datagov;PWD=123",
)
ADDOMAIN = os.environ.get("ADDOMAIN", "EXAMPLEHEALTH")
DC = os.environ.get("DC", "ExampleHealth")
SUFFIX = os.environ.get("SUFFIX", "'DC='" + DC + "',DC=net'")
SEARCHBASES = re.split(
    r"\s*,\s*",
    os.environ.get(
        "SEARCHBASES", "EPIC, Employees, Doctors, Non-Staff, Students, Volunteers"
    ),
)
GROUPSEARCHBASES = re.split(
    r"\s*,\s*",
    os.environ.get(
        "GROUPSEARCHBASES",
        "Email Distribution Groups,    Room & Shared Mailboxes,    Access & Permissions",
    ),
)

USESSL = os.environ.get("USESSL", "true").lower() == "true"
USETLS = os.environ.get("USESSL", "true").lower() == "true"

# https://ldap3.readthedocs.io/


def prefixer(value: str, prefix: str) -> str:
    """Add prefix to value if value exists."""
    if value and value != "":
        return prefix + value

    return value


def get_attribute(attribute: Union[List[str], str], my_data: Dict) -> str:
    """Get LDAP attribute value from data.

    The attribute list can optionally be a list of attributes. The first attribute found is returned.
    """

    def clean_value(value: str) -> str:
        """Clean attribute value."""
        value = value.replace("\u200e", "")
        value = value.replace("smtp:", "")
        value = value.replace("SMTP:", "")
        return value

    current_attrib = ""
    next_attribs = []
    if isinstance(attribute, str):
        current_attrib = attribute
    elif isinstance(attribute, list):
        current_attrib = attribute[0]
        next_attribs = attribute[1:]

    if my_data.get(current_attrib):
        value = my_data.get(current_attrib)
        if isinstance(value, (int, str)):
            return clean_value(str(value))

        if isinstance(value, list):
            return clean_value(value[0])

    if len(next_attribs) > 0:
        return get_attribute(next_attribs, my_data)

    return ""


def main():
    """Primary function."""
    # ssl is optional
    server = Server(SERVERURI, use_ssl=USESSL, get_info=ALL)
    conn = Connection(server, USERNAME, PASSWORD, auto_bind=True, auto_referrals=False)
    if USETLS:
        conn.start_tls()

    """
      1. employee search
          this will create User and Membership table
      2. group search
          this will create the Groups table
    """

    users = []
    memberships = []
    groups = []
    for base in SEARCHBASES:

        # ldap only returns 1000 records at a time. generator will get all.
        generator = conn.extend.standard.paged_search(
            search_base="OU=" + base + "," + SUFFIX,
            search_filter="(CN=*)",
            search_scope=SUBTREE,
            attributes=["*"],
            paged_size=1000,
            generator=True,
        )

        for chunk in generator:
            data = dict(chunk)["attributes"]

            row = [
                base,
                get_attribute("employeeID", data) or "",
                prefixer(get_attribute("sAMAccountName", data), ADDOMAIN + "\\"),
                get_attribute("displayName", data),
                get_attribute(["cn", "name"], data),
                get_attribute("givenName", data),
                get_attribute("sn", data),
                get_attribute("department", data),
                get_attribute(["title", "description"], data),
                get_attribute(["ipPhone", "telephoneNumber"], data),
                get_attribute(["mail", "proxyAddresses", "userPrincipalName"], data),
            ]

            users.append(row)

            if "memberOf" in data:

                for member_set in data["memberOf"]:

                    # one CN
                    cn = re.findall(r"CN=(.+?)(?=,?(?:OU|DC|CN|$))", member_set)[0]

                    # for multiple OUs
                    ou_list = re.findall(r"OU=(.+?)(?=,?(?:OU|DC|CN|$))", member_set)

                    for ou in ou_list:

                        memberrow = [
                            prefixer(
                                get_attribute("sAMAccountName", data), ADDOMAIN + "\\"
                            ),
                            ou,
                            cn,
                        ]

                        # only save three groups
                        if ou in GROUPSEARCHBASES:
                            memberships.append(memberrow)

    for base in GROUPSEARCHBASES:

        # ldap only returns 1000 records at a time. generator will get all.
        generator = conn.extend.standard.paged_search(
            search_base="OU=" + base + "," + SUFFIX,
            search_filter="(CN=*)",
            search_scope=SUBTREE,
            attributes=["*"],
            paged_size=1000,
            generator=True,
        )

        for chunk in generator:
            data = dict(chunk)["attributes"]

            row = [
                base,
                get_attribute("sAMAccountName", data),
                get_attribute("displayName", data),
                get_attribute(["mail", "proxyAddresses", "userPrincipalName"], data),
            ]

            groups.append(row)

    # close connection
    conn.unbind()

    # insert data to db
    conn = pyodbc.connect(DATABASE, autocommit=True)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM [LDAP].[dbo].[Users] where 1=1; DELETE FROM [LDAP].[dbo].[Memberships] where 1=1; DELETE FROM [LDAP].[dbo].[Groups] where 1=1; "
    )
    cursor.executemany(
        "INSERT INTO [LDAP].[dbo].[Users] (Base,EmployeeId,AccountName,DisplayName,FullName,FirstName,LastName,Department,Title,Phone,Email,LoadDate) VALUES (?,?,?,?,?,?,?,?,?,?,?,GetDate())",
        users,
    )
    if len(memberships) > 0:
        cursor.executemany(
            "INSERT INTO [LDAP].[dbo].[Memberships] (AccountName, GroupType, GroupName,LoadDate) VALUES (?,?,?,GetDate())",
            memberships,
        )
    if len(groups) > 0:
        cursor.executemany(
            "INSERT INTO [LDAP].[dbo].[Groups] (GroupType, AccountName, GroupName, GroupEmail,LoadDate) VALUES (?,?,?,?,GetDate())",
            groups,
        )
    conn.close()


if __name__ == "__main__":
    main()
