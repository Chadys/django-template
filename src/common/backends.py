from django.contrib.auth import get_user_model
from django_auth_ldap.backend import LDAPBackend

User = get_user_model()


class CustomUsernameFieldLDAPBackend(LDAPBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Allow for username field different than "username" (example: "email")
        """
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        return super().authenticate(request, username, password, **kwargs)
