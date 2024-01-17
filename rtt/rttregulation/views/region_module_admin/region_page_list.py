import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from rttnews.documents import RegionDocument
from rttproduct.models.models import Industry
from rttcore.permissions import IsSuperUserOrStaff

logger = logging.getLogger(__name__)


class ReactAdminRegionPageApiView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)

    @staticmethod
    def get(request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1217
        """
        try:
            region_doc_qs: RegionDocument = RegionDocument.search().filter(
                'match', region_page=True).source(['id', 'name', 'industries']).sort('name.raw')
            region_doc_qs = region_doc_qs[0: region_doc_qs.count()]

            industry_qs = Industry.objects.all().order_by('name')
            regions = []
            industries = []
            for industry in industry_qs:
                industries.append({
                    'id': industry.id,
                    'name': industry.name,
                })

            for region in region_doc_qs:
                # Activated industry list which are associated with this region
                active_industry_list = {}
                for industry in region.industries:
                    active_industry_list[str(industry.id)] = True

                # All industry list
                industry_list = []
                for industry in industry_qs:
                    if str(industry.id) in active_industry_list:
                        active_status = True
                    else:
                        active_status = False

                    industry_list.append({
                        'id': industry.id,
                        'name': industry.name,
                        'active_status': active_status,
                    })

                regions.append({
                    'id': region.id,
                    'name': region.name,
                    'industries': industry_list
                })
            response = {
                'industries': industries,
                'regions': regions
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
