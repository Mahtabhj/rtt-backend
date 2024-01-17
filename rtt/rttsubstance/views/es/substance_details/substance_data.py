from django.db.models import Sum
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.models import Property, SubstancePropertyDataPoint, PrioritizationStrategyProperty


class SubstanceData(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    def get(self, request, substance_id):
        """
        https://chemycal.atlassian.net/browse/RTT-584
        """

        try:
            organization_id = request.user.organization_id
            properties = Property.objects.filter(
                prioritization_strategy_properties__organization_id=organization_id,
                property_data_property__substance_property_data_point_property_data_point__status='active',
                property_data_property__substance_property_data_point_property_data_point__substance_id=substance_id
            ).distinct().order_by('id')

            property_list = []

            for property_data in properties:
                data = {
                    'id': property_data.id,
                    'name': property_data.name,
                    'short_name': property_data.short_name,
                    'url_link': property_data.url_link,
                    'data_points': []
                }
                substance_property_data_points = SubstancePropertyDataPoint.objects.filter(
                    property_data_point__property__id=property_data.id, status='active',
                    substance_id=substance_id).select_related('property_data_point')
                for data_point in substance_property_data_points:
                    data['data_points'].append({
                        'id': data_point.property_data_point.id,
                        'name': data_point.property_data_point.name,
                        'short_name': data_point.property_data_point.short_name,
                        'value': data_point.value,
                        'image_url': data_point.image.url if data_point.image else None
                    })
                property_list.append(data)

            prioritization = PrioritizationStrategyProperty.objects \
                .filter(property_id__in=properties,
                        prioritization_strategy__organization_id=organization_id) \
                .aggregate(Sum('weight'))['weight__sum']
            response = {
                'prioritization': prioritization,
                'property_list': property_list,
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
