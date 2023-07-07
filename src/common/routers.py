from typing import Iterator

from django.urls import URLPattern
from django.urls import path as django_path
from ninja import Router
from ninja.utils import normalize_path, replace_path_param_notation


class FixRouter(Router):
    def urls_paths(self, prefix: str) -> Iterator[URLPattern]:
        prefix = replace_path_param_notation(prefix)
        for path, path_view in self.path_operations.items():
            path = replace_path_param_notation(path)
            route = "/".join([i for i in (prefix, path) if i])
            # to skip lot of checks we simply treat double slash as a mistake:
            route = normalize_path(route)
            route = route.lstrip("/")
            for operation in path_view.operations:
                url_name = self.api.get_operation_url_name(operation, router=self)

                yield django_path(route, path_view.get_view(), name=url_name)
