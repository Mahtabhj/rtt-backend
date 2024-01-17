import logging
from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from rttnews.documents import RegionDocument

logger = logging.getLogger(__name__)


class RegionDetailsApiView(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request, region_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1035
        """
        try:
            region_doc_qs = RegionDocument.search().filter(
                'match', id=region_id).source(['id', 'name', 'country_flag', 'country_code', 'latitude', 'longitude'])
            region_obj = {}
            for region in region_doc_qs:
                region_obj = {
                    'id': region.id,
                    'name': region.name,
                    'country_code': region.country_code,
                    'country_flag': region.country_flag,
                    'latitude': region.latitude,
                    'longitude': region.longitude,
                }
            if len(region_obj) > 0:
                sub_region_doc_qs = RegionDocument.search().filter(
                    Q('match', parent__id=region_id) &
                    Q('match', region_page=True)
                ).source(['id', 'name', 'country_code', 'latitude', 'longitude'])
                sub_region_doc_qs = sub_region_doc_qs[0:sub_region_doc_qs.count()]
                sub_region_obj_list = []
                for sub_region in sub_region_doc_qs:
                    sub_region_obj_list.append({
                        'id': sub_region.id,
                        'name': sub_region.name,
                        'country_code': sub_region.country_code,
                        'latitude': sub_region.latitude,
                        'longitude': sub_region.longitude,
                    })
                region_obj['sub_regions_count'] = sub_region_doc_qs.count()
                region_obj['sub_regions'] = sub_region_obj_list

            return Response(region_obj, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)