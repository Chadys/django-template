import ldap
from django_auth_ldap.config import LDAPSearch, NestedGroupOfUniqueNamesType

from .base import *

# django-auth-ldap
# urls
LDAP_DOMAIN = env.str("AUTH_LDAP_DOMAIN", default="dc=domain,dc=ovh")
AUTH_LDAP_GROUPS_PARENT_PATH = env.str(
    "AUTH_LDAP_GROUPS_PARENT_PATH", default="ou=groups"
)
AUTH_LDAP_GROUPS_PARENT_PATH = f"{AUTH_LDAP_GROUPS_PARENT_PATH},{LDAP_DOMAIN}"
# Connection
AUTH_LDAP_SERVER_URI = env.str("AUTH_LDAP_SERVER_URI", default="ldap://ldap.domain.ovh")
AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_REFERRALS: 0,
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER,
    ldap.OPT_X_TLS_NEWCTX: 0,
}
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    f"ou=people,{LDAP_DOMAIN}", ldap.SCOPE_SUBTREE, "(|(mail=%(user)s)(uid=%(user)s))"
)
AUTH_LDAP_START_TLS = env.bool("AUTH_LDAP_START_TLS", default=True)
AUTH_LDAP_BIND_DN = env.str("AUTH_LDAP_BIND_DN", default=f"cn=readonly,{LDAP_DOMAIN}")
AUTH_LDAP_BIND_PASSWORD = env.str("AUTH_LDAP_BIND_PASSWORD", default="")
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = env.bool(
    "AUTH_LDAP_BIND_AS_AUTHENTICATING_USER", default=False
)

# Mapping
AUTH_LDAP_ALWAYS_UPDATE_USER = True
# ldap users need to be member of this group to authenticate
AUTH_LDAP_REQUIRE_GROUP = env.str(
    "AUTH_LDAP_REQUIRE_GROUP",
    default="users",
)
AUTH_LDAP_REQUIRE_GROUP = f"cn={AUTH_LDAP_REQUIRE_GROUP},{AUTH_LDAP_GROUPS_PARENT_PATH}"
LDAP_ADMIN_GROUP = env.str(
    "LDAP_ADMIN_GROUP",
    default="admins",
)
LDAP_ADMIN_GROUP = f"cn={LDAP_ADMIN_GROUP},{AUTH_LDAP_GROUPS_PARENT_PATH}"

AUTH_LDAP_USER_ATTR_MAP = env.dict(
    "AUTH_LDAP_USER_ATTR_MAP",
    default={"first_name": "givenName", "last_name": "sn", "email": "mail"},
    subcast=str,
)
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": AUTH_LDAP_REQUIRE_GROUP,
    "is_staff": AUTH_LDAP_REQUIRE_GROUP,
    "is_superuser": LDAP_ADMIN_GROUP,
    "is_from_ldap": AUTH_LDAP_REQUIRE_GROUP,
}
AUTH_LDAP_MIRROR_GROUPS = False
AUTH_LDAP_FIND_GROUP_PERMS = False
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    AUTH_LDAP_GROUPS_PARENT_PATH,
    ldap.SCOPE_SUBTREE,
    "(objectClass=groupOfUniqueNames)",
)
AUTH_LDAP_GROUP_TYPE = NestedGroupOfUniqueNamesType(name_attr="cn")
