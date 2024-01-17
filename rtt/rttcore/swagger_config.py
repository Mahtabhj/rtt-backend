from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url


class Swagger:
    def __init__(self, version, title, is_public, all_permissions, patterns):
        __schema_view = get_schema_view(
            openapi.Info(
                title=title,
                default_version=version
            ),
            public=is_public,
            permission_classes=all_permissions,
            patterns=patterns
        )
        self.__urlpatterns = [
            url(r'^backend/swagger(?P<format>\.json|\.yaml)$', __schema_view.without_ui(cache_timeout=0),
                name='schema-json'),
            url(r'^backend/swagger/$', __schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            url(r'^backend/redoc/$', __schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        ]

    def get_swagger_url(self):
        return self.__urlpatterns
