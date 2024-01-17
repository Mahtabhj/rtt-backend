import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from elasticsearch_dsl import Q

from rttpublicApi.permissions import IsPublicApiAuthorized
from rttlimitManagement.documents import ExemptionDocument
from rttsubstance.models import Substance

logger = logging.getLogger(__name__)


class ExemptionPublicApi(APIView):
    permission_classes = [IsPublicApiAuthorized]

    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-716
        """
        try:
            regulatory_framework_id = request.data.get('regulatory_framework_id', None)
            regulation_id = request.data.get('regulation_id', None)
            substance_id = request.data.get('substance_id', None)
            if not regulatory_framework_id and not regulation_id:
                response_message = {
                    'message': 'Both Regulatory Framework ID and Regulation ID can not be empty'
                }
                return Response(response_message, status=status.HTTP_400_BAD_REQUEST)
            limit = int(request.data.get('limit', 10))
            skip = int(request.data.get('skip', 0))
            results_list = []
            exemption_doc_queryset: ExemptionDocument = ExemptionDocument().search()
            if substance_id:
                substance_id_list = self.get_family_substance_id_list(substance_id)
                exemption_doc_queryset = exemption_doc_queryset.filter(
                    Q('terms', substance__id=substance_id_list)
                )
            '''Filter by framework_id and regulation_id'''
            if regulatory_framework_id and regulation_id:
                # if both framework_id and regulation_id are given, apply OR condition
                exemption_doc_queryset = exemption_doc_queryset.filter(
                    Q('match', regulatory_framework__id=regulatory_framework_id) |
                    Q('match', regulation__id=regulation_id)
                )
            if regulatory_framework_id and not regulation_id:
                # if only framework_id is given, filter by framework_id only
                exemption_doc_queryset = exemption_doc_queryset.filter(
                    Q('match', regulatory_framework__id=regulatory_framework_id)
                )
            if not regulatory_framework_id and regulation_id:
                # if only regulation_id is given, filter by regulation_id only
                exemption_doc_queryset = exemption_doc_queryset.filter(
                    Q('match', regulation__id=regulation_id)
                )

            exemption_doc_queryset = exemption_doc_queryset[skip:limit + skip]
            for exemption in exemption_doc_queryset:
                results_list.append({
                    'substance': {
                        'id': exemption.substance.id,
                        'name': exemption.substance.name,
                        'es': exemption.substance.ec_no,
                        'cas': exemption.substance.cas_no,
                        'is_family': exemption.substance.is_family
                    },
                    'article': exemption.article,
                    'reference': exemption.reference,
                    'application': exemption.application,
                    'expiration_date': exemption.expiration_date,
                    'date_into_force': exemption.date_into_force,
                    'note': exemption.notes,
                    'status': exemption.status,
                })
            response = {
                'count': exemption_doc_queryset.count(),
                'results': results_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_family_substance_id_list(substance_id):
        substance_id_list = [substance_id]
        is_family = Substance.objects.filter(is_family=True, id=substance_id).exists()
        if is_family:
            child_substance_id_list = list(
                Substance.objects.filter(substance_family__family=substance_id).values_list(
                    'id', flat=True))
            substance_id_list.extend(child_substance_id_list)

        return substance_id_list
