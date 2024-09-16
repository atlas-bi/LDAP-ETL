"""Atlas Supplementary LDAP ETL."""
import os
import re
from base64 import b64encode
from typing import Dict, List, Optional, Tuple, Union

import pyodbc
from dotenv import load_dotenv
from ldap3 import ALL, ALL_ATTRIBUTES, SUBTREE, Connection, Server
from ldap3.utils import dn

load_dotenv()

# LDAP connection information
LDAP_HOST = os.environ.get("LDAP_HOST", "ldap.example.com")
LDAP_PASSWORD = os.environ.get("LDAP_PASSWORD", "exampl3")
LDAP_USERNAME = os.environ.get("LDAP_USERNAME", "me")
LDAP_USE_SSL = os.environ.get("LDAP_USE_SSL", "true").lower() == "true"
LDAP_USE_TLS = os.environ.get("LDAP_USE_TLS", "true").lower() == "true"


# LDAP Base
LDAP_BASE = os.environ.get("LDAP_BASE", "dc=example,dc=org")

# LDAP search and attributes
LDAP_GROUP_SEARCH = os.environ.get("LDAP_GROUP_SEARCH", "(objectClass=group)")
LDAP_GROUP_USERNAME = os.environ.get("LDAP_GROUP_USERNAME", "sAMAccountName")
LDAP_GROUP_DISPLAYNAME = os.environ.get("LDAP_GROUP_DISPLAYNAME", "displayName")
LDAP_GROUP_EMAIL = os.environ.get("LDAP_GROUP_EMAIL", "mail")
LDAP_GROUP_OU = os.environ.get("LDAP_GROUP_OU", "")

LDAP_USER_SEARCH = os.environ.get(
    "LDAP_USER_SEARCH", "(&(objectClass=person)(sAMAccountName=*)(givenName=*)(sn=*))"
)
LDAP_USER_EMPLOYEEID = os.environ.get("LDAP_USER_EMPLOYEEID", "employeeID")
LDAP_USER_ACCOUNTNAME = os.environ.get("LDAP_USER_ACCOUNTNAME", "sAMAccountName")
LDAP_USER_DISPLAYNAME = os.environ.get("LDAP_USER_DISPLAYNAME", "displayName")
LDAP_USER_FULLNAME = os.environ.get("LDAP_USER_FULLNAME", "cn,name")
LDAP_USER_FIRSTNAME = os.environ.get("LDAP_USER_FIRSTNAME", "givenName")
LDAP_USER_LASTNAME = os.environ.get("LDAP_USER_LASTNAME", "sn")
LDAP_USER_DEPARTMENT = os.environ.get("LDAP_USER_DEPARTMENT", "department")
LDAP_USER_TITLE = os.environ.get("LDAP_USER_TITLE", "title,description")
LDAP_USER_PHONE = os.environ.get("LDAP_USER_PHONE", "ipPhone,telephoneNumber")
LDAP_USER_EMAIL = os.environ.get(
    "LDAP_USER_EMAIL", "mail,proxyAddresses,userPrincipalName"
)
LDAP_USER_PHOTO = os.environ.get("LDAP_USER_PHOTO", "thumbnailPhoto,profilePhoto")

DATABASE = os.environ.get(
    "DATABASE",
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=atlas;DATABASE=LDAP;UID=datagov;PWD=123",
)

AD_DOMAIN = os.environ.get("AD_DOMAIN", "EXAMPLEHEALTH")


# https://ldap3.readthedocs.io/


def prefixer(value: str, prefix: str) -> str:
    """Add prefix to value if value exists."""
    if value:
        return prefix + value

    return value


def get_ou(dn: List[Tuple[str, ...]]) -> Optional[str]:
    """Get the top OU from a dn."""
    ous = get_ous(dn)
    return get_ous(dn)[-1] if ous else None


def get_ous(dn: List[Tuple[str, ...]]) -> List[str]:
    """Get a list of OUs from a dn."""
    return [x[1] for x in dn if x[0].lower() == "ou"]

def get_cn(dn: List[Tuple[str, ...]]) -> Optional[str]:
    """Get the top CN from a dn."""
    cns = get_cns(dn)
    return get_cns(dn)[-1] if cns else None


def get_cns(dn: List[Tuple[str, ...]]) -> List[str]:
    """Get a list of CNs from a dn."""
    return [x[1] for x in dn if x[0].lower() == "cn"]


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

        if isinstance(value, bytes):
            return b64encode(value).decode("utf-8")

    if len(next_attribs) > 0:
        return get_attribute(next_attribs, my_data)

    return ""


def main():
    """Primary function."""
    server = Server(LDAP_HOST, use_ssl=LDAP_USE_SSL, get_info=ALL)
    conn = Connection(
        server, LDAP_USERNAME, LDAP_PASSWORD, auto_bind=True, auto_referrals=False
    )
    if LDAP_USE_TLS:
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

    generator = conn.extend.standard.paged_search(
        LDAP_BASE,
        search_filter=LDAP_USER_SEARCH,
        search_scope=SUBTREE,
        attributes=ALL_ATTRIBUTES,
        paged_size=100,
        generator=True,
    )

    for chunk in generator:
        data = dict(chunk)

        if "attributes" not in data:
            continue

        attributes = data["attributes"]
        # mang = ""
        # if "manager" in attributes:
        #     for mgr in attributes["manager"]:
        #             # one CN
        #             try:
        #                 mang = re.findall(r"CN=(.+?)(?=,?(?:OU|DC|CN|$))", mgr)[-1]
        #             except:
        #                 pass
        # if "manager" in attributes:
            # try:
            #     mang = re.findall(r"CN=(.+?)(?=,?(?:OU|DC|CN|$))", attributes["manager"])
            # except:
            #     pass
        row = [
            get_attribute(LDAP_USER_EMPLOYEEID.split(","), attributes) or "",
            prefixer(
                get_attribute(LDAP_USER_ACCOUNTNAME.split(","), attributes),
                AD_DOMAIN + "\\",
            ),
            get_attribute(LDAP_USER_DISPLAYNAME.split(","), attributes),
            get_attribute(LDAP_USER_FULLNAME.split(","), attributes),
            get_attribute(LDAP_USER_FIRSTNAME.split(","), attributes),
            get_attribute(LDAP_USER_LASTNAME.split(","), attributes),
            get_attribute(LDAP_USER_DEPARTMENT.split(","), attributes),
            get_attribute(LDAP_USER_TITLE.split(","), attributes),
            get_attribute(LDAP_USER_PHONE.split(","), attributes),
            get_attribute(LDAP_USER_EMAIL.split(","), attributes),
            get_attribute(LDAP_USER_PHOTO.split(","), attributes),
            # mang,
            get_cn(
                    dn.parse_dn(
                        get_attribute(["manager", "dn"], attributes)
                        or LDAP_BASE
                    )
                ),  # tallest ou is used.
        ]

        users.append(row)

        if "memberOf" in attributes:
            for member_set in attributes["memberOf"]:
                # one CN
                cn = re.findall(r"CN=(.+?)(?=,?(?:OU|DC|CN|$))", member_set)[0]
                # for multiple OUs
                ou_list = re.findall(r"OU=(.+?)(?=,?(?:OU|DC|CN|$))", member_set)

                for ou in ou_list:
                    memberrow = [
                        prefixer(
                            get_attribute("sAMAccountName", attributes),
                            AD_DOMAIN + "\\",
                        ),
                        ou,
                        cn,
                    ]

                    if not LDAP_GROUP_OU or ou in LDAP_GROUP_OU.split(","):
                        memberships.append(memberrow)

    generator = conn.extend.standard.paged_search(
        LDAP_BASE,
        search_filter=LDAP_GROUP_SEARCH,
        search_scope=SUBTREE,
        attributes=ALL_ATTRIBUTES,
        paged_size=100,
        generator=True,
    )

    for chunk in generator:
        data = dict(chunk)
        if "attributes" not in data:
            continue

        attributes = data["attributes"]

        ous = get_ous(
            dn.parse_dn(
                get_attribute(["distinguishedName", "dn"], attributes) or LDAP_BASE
            )
        )

        # if we have a custom AD OU filter
        if not LDAP_GROUP_OU or (
            LDAP_GROUP_OU and list(set(LDAP_GROUP_OU.split(",")) & set(ous))
        ):
            row = [
                get_ou(
                    dn.parse_dn(
                        get_attribute(["distinguishedName", "dn"], attributes)
                        or LDAP_BASE
                    )
                ),  # tallest ou is used.
                get_attribute(LDAP_GROUP_USERNAME.split(","), attributes),
                get_attribute(LDAP_GROUP_DISPLAYNAME.split(","), attributes),
                get_attribute(LDAP_GROUP_EMAIL.split(","), attributes),
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
        "INSERT INTO [LDAP].[dbo].[Users] (EmployeeId,AccountName,DisplayName,FullName,FirstName,LastName,Department,Title,Phone,Email,Photo,Manager,LoadDate) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,GetDate())",
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
