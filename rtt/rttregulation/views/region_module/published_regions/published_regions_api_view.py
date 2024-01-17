from elasticsearch_dsl import Q

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from rttnews.documents import RegionDocument
from rttproduct.models.core_models import Industry

logger = logging.getLogger(__name__)


class ActiveRegionPagesApiView(APIView):
    permission_classes = (IsAuthenticated, )

    @staticmethod
    def get(request):
        """
          doc: https://chemycal.atlassian.net/browse/RTT-1065
        """
        try:
            organization_id = request.user.organization_id
            industry_id_list = list(Industry.objects.filter(organization_industries__id=organization_id).values_list(
                'id', flat=True))
            region_doc_qs: RegionDocument = RegionDocument.search().filter(
                Q('match', region_page=True) &
                Q('nested',
                  path='industries',
                  query=Q('terms', industries__id=industry_id_list))
            ).source(['id'])
            region_doc_qs = region_doc_qs[0: region_doc_qs.count()]

            response = []
            for region in region_doc_qs:
                response.append(region.id)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
