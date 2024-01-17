from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from elasticsearch_dsl import Q
import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rttcore.permissions import IsActiveLimitsManagementModule
from rest_framework.response import Response
from rest_framework import status

from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttsubstance.documents import SubstanceDocument

logger = logging.getLogger(__name__)


class SubstanceLimitFilterOption(APIView):
    permission_classes = [IsAuthenticated, IsActiveLimitsManagementModule]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'substances': openapi.Schema(type=openapi.TYPE_ARRAY,
                                         description='List of substances IDs',
                                         items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'uses_and_applications': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                    description='List of UseAndApplications IDs',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regions IDs',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Framework IDs',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulations IDs',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'substance_search': openapi.Schema(type=openapi.TYPE_STRING,
                                               description='Keyword, which will be searched in substance name'),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in substance name, scope and region name'),
            'from_date': openapi.Schema(type=openapi.TYPE_STRING,
                                        description='Last modified from data(yyyy-mm-dd)'),
            'to_date': openapi.Schema(type=openapi.TYPE_STRING,
                                      description='Last modified to data(yyyy-mm-dd)'),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-670?focusedCommentId=11688
        """
        try:
            filters = {
                'substances': request.data.get('substances', None),
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'regions': request.data.get('regions', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'regulations': request.data.get('regulations', None),
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None)
            }
            response = []
            substance_search_keyword = request.data.get('substance_search', None)
            # the user should add at least 4 chars, and we will return matching substances
            if substance_search_keyword and len(substance_search_keyword) > 3:
                search_keyword = request.data.get('search', None)
                organization_id = request.user.organization_id
                regulatory_frameworks_ids = []
                regulations_ids = []
                if filters.get('uses_and_applications', None):
                    substances_id = LimitCoreService().get_substances_ids(filters.get('uses_and_applications', None))
                    if not filters.get('substances', None):
                        filters['substances'] = []
                    filters['substances'] = list(set(filters['substances'] + substances_id))

                if filters.get('regulatory_frameworks', None) or (not filters.get('regulatory_frameworks', None) and
                                                                  not filters.get('regulations', None)):
                    framework_doc_qs = LimitCoreService().get_framework_limit_queryset(organization_id, filters,
                                                                                       search_keyword)
                    framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
                    for framework in framework_doc_qs:
                        if len(framework.regions) > 0:
                            regulatory_frameworks_ids.append(framework.id)
                if filters.get('regulations', None) or (not filters.get('regulatory_frameworks', None) and
                                                        not filters.get('regulations', None)):
                    regulation_doc_qs = LimitCoreService().get_regulation_limit_queryset(organization_id, filters,
                                                                                         search_keyword)
                    regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
                    for regulation in regulation_doc_qs:
                        if regulation.regulatory_framework and len(regulation.regulatory_framework.regions) > 0:
                            regulations_ids.append(regulation.id)

                substance_doc_qs: SubstanceDocument = SubstanceDocument.search().filter(
                    Q('nested',
                      path='regulation_substance_limit',
                      query=Q('terms',
                              regulation_substance_limit__regulatory_framework__id=regulatory_frameworks_ids)) |
                    Q('nested',
                      path='regulation_substance_limit',
                      query=Q('terms',
                              regulation_substance_limit__regulation__id=regulations_ids))
                ).query(
                    Q('match', name=substance_search_keyword) |
                    Q('match_phrase', cas_no=substance_search_keyword) |
                    Q('match_phrase', ec_no=substance_search_keyword)
                ).sort("_score")
                substance_doc_qs = substance_doc_qs[0:substance_doc_qs.count()]
                for substance in substance_doc_qs:
                    response.append({
                        'id': substance.id,
                        'name': substance.name,
                        'cas_no': substance.cas_no,
                        'ec_no': substance.ec_no,
                    })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
