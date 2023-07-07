import os

from django.conf import settings
from ninja.errors import ConfigError
from ninja.main import NinjaAPI, debug_server_url_reimport
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from common.api import router as common_router
from common.parsers import ORJSONParser
from common.renderers import ORJSONRenderer


class DevNinjaExtraAPI(NinjaExtraAPI):
    def _validate(self) -> None:
        # 1) urls namespacing validation
        skip_registry = os.environ.get("NINJA_SKIP_REGISTRY", False)
        if (
            not skip_registry
            and self.urls_namespace in NinjaAPI._registry
            and not debug_server_url_reimport()
        ):
            msg = [
                "Looks like you created multiple NinjaAPIs or TestClients",
                "To let ninja distinguish them you need to set either unique version or url_namespace",
                " - NinjaAPI(..., version='2.0.0')",
                " - NinjaAPI(..., urls_namespace='otherapi')",
                f"Already registered: {NinjaAPI._registry}",
            ]
            raise ConfigError("\n".join(msg))
        NinjaAPI._registry.append(self.urls_namespace)


if settings.NINJA_DJANGO_AUTH:
    api = DevNinjaExtraAPI(
        parser=ORJSONParser(),
        renderer=ORJSONRenderer(),
        title=f"{settings.SITE_NAME} API",
        version=settings.API_VERSION,
    )
else:
    api = NinjaExtraAPI(
        parser=ORJSONParser(),
        renderer=ORJSONRenderer(),
        title=f"{settings.SITE_NAME} API",
        version=settings.API_VERSION,
    )
api.register_controllers(NinjaJWTDefaultController)

api.add_router("", common_router)
