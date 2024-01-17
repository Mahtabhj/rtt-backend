from django.db.models import Sum
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.models import Property, PropertyDataPoint, PrioritizationStrategyProperty, PrioritizationStrategy
from rttsubstance.services.substance_core_service import SubstanceCoreService

logger = logging.getLogger(__name__)


class PropertyPrioritizedSubstanceData(APIView):
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
            'sort_field': openapi.Schema(type=openapi.TYPE_STRING, enum=['name', 'prioritization', 'property'],
                                         description='sort by filed name'),
            'sort_order': openapi.Schema(type=openapi.TYPE_STRING, enum=['asc', 'desc'],
                                         description='sort data in asc or desc order'),
            'property_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='property id'),
            'prioritization_strategies': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                        description='List of prioritization_strategies ID',
                                                        items=openapi.Schema(type=openapi.TYPE_INTEGER))
        }
    ))
    def post(self, request):
        """
        https://chemycal.atlassian.net/browse/RTT-637
        """
        try:
            filters = {
                'uses_and_applications': request.data.get('uses_and_applications', None),
                'products': request.data.get('products', None),
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'prioritization_strategies': request.data.get('prioritization_strategies', None)
            }
            search_keyword = request.data.get('search', None)
            sort_field = request.data.get('sort_field', 'mentioned').lower()
            sort_order = request.data.get('sort_order', 'desc').lower()
            property_id = request.data.get('property_id', None)
            organization_id = request.user.organization_id
            name_sort_order = 'asc'
            if sort_field == 'name':
                name_sort_order = sort_order
            default_org_strategy_id = None
            if filters.get('prioritization_strategies', None):
                default_org_strategy_id = filters['prioritization_strategies'][0]
            else:
                default_org_strategy = PrioritizationStrategy.objects.filter(
                    organization_id=organization_id, default_org_strategy=True,
                    properties__property_data_property__substance_property_data_point_property_data_point__status='active')
                if not filters.get('prioritization_strategies', None) and default_org_strategy.count() < 1:
                    return Response({"message": "No default prioritization_strategies found for this organization"},
                                    status=status.HTTP_400_BAD_REQUEST)
                default_org_strategy = default_org_strategy.first()
                default_org_strategy_id = default_org_strategy.id
            default_org_strategy = PrioritizationStrategy.objects.filter(
                id=default_org_strategy_id).first()
            default_org_strategy_name = default_org_strategy.name
            property_prioritized_substance_list = SubstanceCoreService().get_filtered_substance_queryset(
                organization_id=organization_id,
                property_prioritized=True,
                filters=filters,
                search_keyword=search_keyword,
                sort_field='name',
                sort_order=name_sort_order)

            property_prioritized_substance_list = property_prioritized_substance_list[
                                                  0:property_prioritized_substance_list.count()]

            '''
            sort substance by property present/not present
            https://chemycal.atlassian.net/browse/RTT-569
            '''
            if sort_field == 'property' and property_id:
                property_datapoint_ids = list(
                    PropertyDataPoint.objects.filter(
                        property_id=property_id, substance_property_data_point_property_data_point__status='active'
                    ).values_list('id', flat=True))
                property_prioritized_substance_list = property_prioritized_substance_list.sort(
                    {"substance_property_data_point_relation.property_data_point.id": {
                        "order": sort_order,
                        "missing": 0,
                        "nested": {
                            "path": "substance_property_data_point_relation",
                            "filter": {
                                "terms": {
                                    "substance_property_data_point_relation.property_data_point.id": property_datapoint_ids
                                }
                            }
                        }
                    }
                    })

            results = []
            if filters.get('prioritization_strategies', None):
                organization_property_ids = list(Property.objects.filter(
                    prioritization_strategy_properties__id__in=filters['prioritization_strategies'],
                    prioritization_strategy_properties__organization_id=organization_id).values_list('id', flat=True))
            else:
                organization_property_ids = list(Property.objects.filter(
                    prioritization_strategy_properties__id=default_org_strategy_id,
                    prioritization_strategy_properties__organization_id=organization_id).values_list('id', flat=True))
            for substance in property_prioritized_substance_list:
                properties = list(Property.objects.filter(
                    id__in=organization_property_ids,
                    property_data_property__substance_property_data_point_property_data_point__substance_id=substance.id,
                    property_data_property__substance_property_data_point_property_data_point__status='active')
                                  .distinct().order_by('id').values_list('id', flat=True))
                prioritization = PrioritizationStrategyProperty.objects \
                    .filter(property_id__in=properties,
                            prioritization_strategy__organization_id=organization_id) \
                    .aggregate(Sum('weight'))['weight__sum']
                data = {
                    "id": substance.id,
                    "name": substance.name,
                    "prioritization": prioritization if prioritization else 0,
                    "properties": properties,
                }

                results.append(data)

            if sort_field == 'prioritization':
                results = sorted(results, key=lambda i: i['prioritization'],
                                 reverse=True if sort_order == 'desc' else False)

            response = {
                "count": property_prioritized_substance_list.count(),
                "results": results,
                "prioritization_strategies": {
                    "id": default_org_strategy_id,
                    "name": default_org_strategy_name,
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
