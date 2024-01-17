import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from rttnews.documents import RegionDocument

logger = logging.getLogger(__name__)


class RegionListApiView(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request):
        """
          doc: https://chemycal.atlassian.net/browse/RTT-1043
        """
        try:
            region_doc_qs: RegionDocument = RegionDocument.search().filter(
                'match', region_page=True).source(['id', 'name', 'country_code', 'latitude', 'longitude'])
            region_doc_qs = region_doc_qs[0: region_doc_qs.count()]

            response = []
            for region in region_doc_qs:
                response.append({
                    'id': region.id,
                    'name': region.name,
                    'country_code': region.country_code,
                    'latitude': region.latitude,
                    'longitude': region.longitude,
                })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)