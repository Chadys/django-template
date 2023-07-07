from django.conf import settings


def extra_settings_exposed(request=None):
    return {
        "site_name": settings.SITE_NAME,
        "debug": settings.DEBUG,
    }
