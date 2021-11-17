"""Atlas Supplementary LDAP ETL."""
from typing import Dict, List, Union

import pyodbc
from ldap3 import ALL, SUBTREE, Connection, Server

import settings

# https://ldap3.readthedocs.io/

# ssl is optional
server = Server(settings.server_uri, use_ssl=True, get_info=ALL)
conn = Connection(
    server, settings.username, settings.password, auto_bind=True, auto_referrals=False
)
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


for base in settings.search_bases:

    # ldap only returns 1000 records at a time. generator will get all.
    generator = conn.extend.standard.paged_search(
        search_base="OU=" + base + ",dc=" + settings.dc + ",dc=net",
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
            get_attribute("employeeID", data),
            prefixer(get_attribute("sAMAccountName", data), settings.ad_domain + "\\"),
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
                memberdict = dict([x.split("=") for x in member_set.split(",")])

                memberrow = [
                    prefixer(
                        get_attribute("sAMAccountName", data), settings.ad_domain + "\\"
                    ),
                    get_attribute("OU", memberdict),
                    get_attribute("CN", memberdict),
                ]

                # only save three groups
                if (
                    "OU" in memberdict
                    and memberdict["OU"] in settings.group_search_bases
                ):
                    memberships.append(memberrow)


for base in settings.group_search_bases:

    # ldap only returns 1000 records at a time. generator will get all.
    generator = conn.extend.standard.paged_search(
        search_base="OU=" + base + ",dc=" + settings.dc + ",dc=net",
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
conn = pyodbc.connect(settings.database, autocommit=True)
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
