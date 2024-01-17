from elasticsearch_dsl import Q
import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rttcore.permissions import IsActiveLimitsManagementModule
from rest_framework.response import Response
from rest_framework import status

from rttcore.services.id_search_service import IdSearchService
from rttlimitManagement.documents import ExemptionDocument
from rttsubstance.models import Substance
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService

logger = logging.getLogger(__name__)


class LimitExemptionAPIView(APIView):
    permission_classes = [IsAuthenticated, IsActiveLimitsManagementModule]

    def get(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-656
        """
        try:
            organization_id = request.user.organization_id
            regulation_id = request.GET.get('regulation_id')
            is_regulation = request.GET.get('is_regulation', 'false')
            substance_id = request.GET.get('substance_id')
            limit = int(request.GET.get('limit', 20))
            skip = int(request.GET.get('skip', 0))
            search_keyword = request.GET.get('search', None)
            exemptions_list = []
            relevant_substance_ids = RelevantSubstanceService().get_organization_relevant_substance_ids(organization_id)
            exemption_search_qs = self.get_exemption_search_queryset(regulation_id, is_regulation, substance_id,
                                                                     search_keyword)
            count = exemption_search_qs.count()
            exemption_search_qs = exemption_search_qs[skip:skip + limit]
            for exemption in exemption_search_qs:
                exemptions_list.append({
                    'id': exemption.id,
                    'article': exemption.article,
                    'reference': exemption.reference,
                    'application': exemption.application,
                    'status': exemption.status,
                    'expiration_date': exemption.expiration_date,
                    'substance': {
                        'id': exemption.substance.id,
                        'name': exemption.substance.name,
                        'cas_no': exemption.substance.cas_no,
                        'ec_no': exemption.substance.ec_no,
                        'is_relevant': IdSearchService().does_id_exit_in_sorted_list(relevant_substance_ids,
                                                                                     exemption.substance.id)
                    },
                    'notes': exemption.notes if exemption.notes else None
                })
            response = {
                'count': count,
                'results': exemptions_list,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_exemption_search_queryset(regulation_id, is_regulation, substance_id, search_keyword=None):
        substance_id_list = [substance_id]
        is_family = Substance.objects.filter(is_family=True, id=substance_id).exists()
        if is_family:
            child_substance_id_list = list(Substance.objects.filter(substance_family__family=substance_id).values_list(
                'id', flat=True))
            substance_id_list.extend(child_substance_id_list)

        if is_regulation.lower() == 'true':
            exemption_doc_qs: ExemptionDocument = ExemptionDocument.search().filter('match', status='active').filter(
                Q('terms', substance__id=substance_id_list) &
                Q('match', regulation__id=regulation_id)
            )
        else:
            exemption_doc_qs: ExemptionDocument = ExemptionDocument.search().filter('match', status='active').filter(
                Q('terms', substance__id=substance_id_list) &
                Q('match', regulatory_framework__id=regulation_id)
            )
        # filter by search_keyword
        if search_keyword:
            exemption_doc_qs = exemption_doc_qs.query(
                Q('match', substance__name=search_keyword) |
                Q('match_phrase', substance__ec_no=search_keyword) |
                Q('match_phrase', substance__cas_no=search_keyword) |
                Q('match', substance__ec_no=search_keyword) | Q('match', substance__cas_no=search_keyword) |
                Q('match', application=search_keyword) |
                Q('match', article=search_keyword) |
                Q('match', reference=search_keyword)
            )
        return exemption_doc_qs
