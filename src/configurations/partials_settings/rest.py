from .base import *  # noqa

# django rest framework
NINJA_JWT = {
    # env timedelta assumes value is an integer in seconds
    "ACCESS_TOKEN_LIFETIME": env.timedelta(
        "ACCESS_TOKEN_LIFETIME", default=432000 if DEBUG else 300
    ),  # dev: 5 days, prod: 5min
    "REFRESH_TOKEN_LIFETIME": env.timedelta(
        "REFRESH_TOKEN_LIFETIME", default=864000 if DEBUG else 14400
    ),  # dev: 10 days, prod: 4h
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS512",
    "SIGNING_KEY": env.str("NINJA_JWT_SIGNING_KEY"),
    "UPDATE_LAST_LOGIN": False,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "username",
    "USER_AUTHENTICATION_RULE": "ninja_jwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("ninja_jwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "ninja_jwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}
API_URL_PREFIX = add_ending_slash(env.str("API_URL_PREFIX", default="api/"))
API_VERSION = "v1"
