"""
Django settings for #project_name project.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .partials_settings.base import *  # noqa
from .partials_settings.ldap import *  # noqa
from .partials_settings.rest import *  # noqa
from .partials_settings.security import *  # noqa

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django_filters",
    "corsheaders",
    "ninja",
    "ninja_jwt",
    "ninja_jwt.token_blacklist",
    "ninja_extra",
    "common",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "configurations.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "common.context_processors.extra_settings_exposed",
            ],
        },
    },
]


STATIC_ROOT = BASE_DIR / "public" / "static"
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / "public" / "media"
MEDIA_URL = "/media/"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": env.dj_db_url("DATABASE_URL")}
# used by bulk operations
DEFAULT_BATCH_SIZE = env.int("DEFAULT_BATCH_SIZE", default=10000)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Get loglevel from env
LOGLEVEL = env.str("LOGLEVEL", default="WARNING").upper()
SQL_LOGLEVEL = env.str("SQL_LOGLEVEL", default=LOGLEVEL)
LOG_FORMAT = env.str(
    "LOG_FORMAT",
    default="[{levelname}] <{asctime}> {pathname}:{lineno} {message}",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "formatters": {
        "verbose": {
            "format": LOG_FORMAT,
            "style": "{",
        },
    },
    "loggers": {
        # root logger, for third party and such
        "": {
            "level": LOGLEVEL,
            "handlers": [
                "console",
            ],
        },
        "django": {
            "level": LOGLEVEL,
            "handlers": ["console"],
            # required to avoid double logging with root logger
            "propagate": False,
        },
        # django database logs
        "django.db.backends": {
            "level": SQL_LOGLEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "django_auth_ldap": {
            "level": SQL_LOGLEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True


SENTRY_DSN = env.str("SENTRY_DSN", default=None)
SENTRY_TRACES_SAMPLE_RATE = env.int("SENTRY_TRACES_SAMPLE_RATE", default=0.0)
SENTRY_DEBUG = env.bool("SENTRY_DEBUG", default=DEBUG)
if SENTRY_DSN and ENV_MODE != EnvMode.TEST:
    # SENTRY_DSN and SENTRY_ENVIRONMENT is read directly in env var by init
    sentry_sdk.init(
        integrations=[DjangoIntegration(), RedisIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,
        debug=SENTRY_DEBUG,
    )
