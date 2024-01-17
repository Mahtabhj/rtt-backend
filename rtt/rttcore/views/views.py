from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
import subprocess
from elasticsearch_dsl.connections import connections

from rttcore.permissions import IsSuperUserOrStaff


class DefaultResultsSetPagination(PageNumberPagination):
    page_size = 999999
    page_size_query_param = 'pageSize'
    max_page_size = 100000
    page_query_param = 'pageNumber'


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class ElasticSearchRebuild(APIView):
    permission_classes = [IsSuperUserOrStaff]

    @staticmethod
    @swagger_auto_schema(
        operation_description='Rebuild elasticsearch data. Delete the indices and then recreate and populate them.',
        manual_parameters=[openapi.Parameter(
            name="models",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False,
            description="Specify the model or app to be updated in elasticsearch. "
                        "If no model provided all models will be rebuilt."
                        "<small>format: [app[.model] [app[.model] ...]]</small>"
        )]
    )
    def get(request):
        try:
            # conn = connections.create_connection(hosts='localhost:9200')
            # print(conn)
            models = request.GET.get('models', None)
            if models:
                p = subprocess.call(['bash', './rebuild.sh', models])
                output = subprocess.check_output(['bash', './rebuild.sh', models])
            else:
                p = subprocess.call(['bash', './rebuild.sh'])
                output = subprocess.check_output(['bash', './rebuild.sh'])
            return Response({"data": str(output.decode())})
        except Exception as e:
            print(str(e))
            return Response({"data": str(e)})


class ElasticSearchPopulate(APIView):
    permission_classes = [IsSuperUserOrStaff]

    @staticmethod
    @swagger_auto_schema(
        operation_description='Populate elasticsearch data. Populate elasticsearch indices with models data. '
                              'this will not delete indices.',
        manual_parameters=[openapi.Parameter(
            name="models",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False,
            description="Specify the model or app to be updated in elasticsearch. "
                        "If no model provided all models will be populated."
                        "<small>format: [app[.model] [app[.model] ...]]</small>"
        )]
    )
    def get(request):
        try:
            # conn = connections.create_connection(hosts='localhost:9200')
            # print(conn)
            models = request.GET.get('models', None)
            if models:
                p = subprocess.call(['bash', './populate.sh', models])
                output = subprocess.check_output(['bash', './populate.sh', models])
            else:
                p = subprocess.call(['bash', './populate.sh'])
                output = subprocess.check_output(['bash', './populate.sh'])
            return Response({"data": str(output.decode())})
        except Exception as e:
            print(str(e))
            return Response({"data": str(e)})


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if getattr(exc, 'default_code', False) in ['not_authenticated', 'token_not_valid']:
        response.status_code = status.HTTP_403_FORBIDDEN

    return response
