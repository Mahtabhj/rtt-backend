from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.substance_core_service import SubstanceCoreService

logger = logging.getLogger(__name__)


class PrioritizedStrategyFilterOptions(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'uses_and_applications': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                    description='List of uses_and_applications ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Product ID',
                                       items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of Framework ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='search by name, ec_no and cas_no'),
            'prioritization_strategies': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                        description='List of prioritization_strategies ID',
                                                        items=openapi.Schema(type=openapi.TYPE_INTEGER))
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1315
        """
        try:
            filters = {
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'products': request.data.get('products', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'prioritization_strategies': request.data.get('prioritization_strategies', None)
            }
            search_keyword = request.data.get('search', None)
            organization_id = request.user.organization_id
            substance_doc_qs = SubstanceCoreService().get_filtered_substance_queryset(
                organization_id=organization_id,
                property_prioritized=True,
                filters=filters,
                search_keyword=search_keyword,
                sort_field='name',)

            substance_doc_qs = substance_doc_qs[0:substance_doc_qs.count()]
            relevant_property_datapoint_ids = set()
            for substance in substance_doc_qs:
                for substance_property_data_point in substance.substance_property_data_point_relation:
                    if substance_property_data_point.property_data_point and substance_property_data_point.status == 'active':
                        relevant_property_datapoint_ids.add(substance_property_data_point.property_data_point.id)

            prioritization_strategies_list = SubstanceCoreService().get_prioritization_strategies_queryset(
                organization_id, list(relevant_property_datapoint_ids), serializer=True)
            response = {
                "prioritization_strategies": prioritization_strategies_list,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
