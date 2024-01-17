import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.services.regulatory_framework_content_service import RegulatoryFrameworkContentService

logger = logging.getLogger(__name__)


class RegulationMapAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-809
        """
        try:
            topics = request.data.get('topics', None)
            regions = request.data.get('regions', None)
            products = request.data.get('product_categories', None)
            materials = request.data.get('material_categories', None)
            reg_status = request.data.get('status', None)
            region_results = []
            organization_id = request.user.organization_id
            framework_content_service = RegulatoryFrameworkContentService(organization_id)
            queryset_regulatory = framework_content_service.get_filtered_regulatory_framework_queryset(
                topics, products, materials, regions, status=reg_status)
            queryset_regulatory = queryset_regulatory[0:queryset_regulatory.count()]
            for regulatory in queryset_regulatory:
                self.prepare_data(regulatory.regions, region_results, regulatory)
            return Response({'regions': region_results}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Server error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def is_id_exists_in_list(list_data, id):
        """
        Return found and index.
        """
        for index, item in enumerate(list_data):
            if item['id'] == id:
                return True, index
        return False, -1

    def prepare_data(self, source_data, result_data, area_obj):
        for data in source_data:
            found, index = self.is_id_exists_in_list(result_data, data.id)
            if found:
                result_data[index]['selected_ids'].append(area_obj.id)
                result_data[index]['total_length'] += 1
            else:
                temp = {
                    'id': data.id,
                    'title': data.name,
                    'country_code': data.country_code,
                    'latitude': data.latitude,
                    'longitude': data.longitude,
                    'total_length': 1,
                    'selected_ids': []
                }

                temp['selected_ids'].append(area_obj.id)
                result_data.append(temp)
