import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttregulation.services.what_next_milestone_service import WhatNextMilestoneService
from rttnews.documents import RegionDocument
from rttregulation.services.regulation_tagged_region_service import RegulationTaggedRegionService
logger = logging.getLogger(__name__)


class WhatsNextMapAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1333
        """
        try:
            period = str(request.data.get('period', ''))
            filters = {
                'period_start': period + '-01-01' if period else None,
                'period_end': period + '-12-31' if period else None,
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'regulations': request.data.get('regulations', None),
                'milestone_types': request.data.get('milestone_types', None),
                'regions': request.data.get('regions', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'related_products': request.data.get('related_products', None),
                'status': request.data.get('status', None),
                'topics': request.data.get('topics', None)
            }
            response = []
            visited_region = {}
            organization_id = request.user.organization_id
            search_keyword = request.data.get('search', None)
            queryset_milestone = WhatNextMilestoneService().get_what_next_filtered_milestone_document_queryset(
                organization_id, filters, search_keyword)
            queryset_milestone = queryset_milestone[0:queryset_milestone.count()]
            for milestone in queryset_milestone:
                if milestone.regulation:
                    if milestone.regulation.regulatory_framework:
                        regions = RegulationTaggedRegionService().get_region_data(
                            milestone.regulation.regulatory_framework.id, serializer=False)
                        self.prepare_data(regions, visited_region, response, milestone.regulation.id,
                                          is_regulation=True)
                elif milestone.regulatory_framework:
                    self.prepare_data(milestone.regulatory_framework.regions, visited_region, response,
                                      milestone.regulatory_framework.id, is_regulation=False)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def prepare_data(regions, visited_region, response, regulation_id, is_regulation=False):
        for region in regions:
            if not str(region.id) in visited_region:
                region_doc_qs = RegionDocument.search().filter('match', id=region.id)
                region_doc_qs = region_doc_qs[0:region_doc_qs.count()]
                region_doc_obj = None
                for region_data in region_doc_qs:
                    region_doc_obj = region_data
                region_obj = {
                    'id': region_doc_obj.id,
                    'title': region_doc_obj.name,
                    'country_code': region_doc_obj.country_code,
                    'latitude': region_doc_obj.latitude,
                    'longitude': region_doc_obj.longitude,
                    'total_length': 0,
                    'regulations': set(),
                    'regulatory_frameworks': set()
                }
                visited_region[str(region.id)] = len(response)
                response.append(region_obj)
            idx = visited_region[str(region.id)]
            response[idx]['total_length'] += 1
            if is_regulation:
                response[idx]['regulations'].add(regulation_id)
            else:
                response[idx]['regulatory_frameworks'].add(regulation_id)
