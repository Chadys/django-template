import functools
import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from ninja.security import django_auth
from ninja_extra.exceptions import NotFound
from ninja_jwt.authentication import JWTAuth

logger = logging.getLogger(__name__)

AUTH = [JWTAuth(), django_auth] if settings.NINJA_DJANGO_AUTH else [JWTAuth()]


def does_not_exist_raise_404(func):
    @functools.wraps(func)
    def execute(*args, **kwarg):
        try:
            return func(*args, **kwarg)
        except ObjectDoesNotExist:
            raise NotFound()

    return execute
