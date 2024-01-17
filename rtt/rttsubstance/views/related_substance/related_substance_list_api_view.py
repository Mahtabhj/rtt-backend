from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttsubstance.models import Substance
from django.db.models import Q

logger = logging.getLogger(__name__)


class RelatedSubstanceFromRDSListAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regulation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='enter regulation_id'),
            'regulatory_framework_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='enter '
                                                                                             'regulatory_framework_id'),
            'milestone_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='enter milestone_id'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='limit for pagination'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER, description='start position for pagination')
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-941
        """
        try:
            search_keyword = request.data.get('search', '')
            regulation_id = request.data.get('regulation_id', None)
            regulatory_framework_id = request.data.get('regulatory_framework_id', None)
            milestone_id = request.data.get('milestone_id', None)
            id_count = [request.data.get('regulation_id', 0), request.data.get('regulatory_framework_id', 0),
                        request.data.get('milestone_id', 0)]
            if id_count.count(0) > len(id_count) - 1:
                return Response({"message": "regulation_id AND regulatory_framework_id AND milestone_id all can not be "
                                            "empty"}, status=status.HTTP_400_BAD_REQUEST)
            elif id_count.count(0) < len(id_count) - 1:
                return Response({"message": "Only regulation_id OR regulatory_framework_id OR milestone_id can be "
                                            "sent"}, status=status.HTTP_400_BAD_REQUEST)
            if regulation_id:
                substance_qs = Substance.objects.filter(substances_regulation__id=regulation_id).prefetch_related(
                    'uses_and_application_substances')
            elif regulatory_framework_id:
                substance_qs = Substance.objects.filter(substances_regulatory_framework__id=regulatory_framework_id).\
                    prefetch_related('uses_and_application_substances')
            else:
                substance_qs = Substance.objects.filter(substances_regulation_milestone__id=milestone_id).\
                    prefetch_related('uses_and_application_substances')

            if len(search_keyword) > 0:
                substance_qs = substance_qs.filter(Q(name__icontains=search_keyword) |
                                                   Q(ec_no__icontains=search_keyword) |
                                                   Q(cas_no__icontains=search_keyword))

            count = substance_qs.count()
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            substance_qs = substance_qs[skip:skip + limit]
            response = {
                'count': count,
                'results': self.get_substance_and_organization(substance_qs)
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_substance_and_organization(substance_qs):
        result = []
        for substance in substance_qs:
            substance_obj = {
                'id': substance.id,
                'name': substance.name,
                'ec_no': substance.ec_no,
                'cas_no': substance.cas_no,
                'organization': []
            }
            visited_organization = {}
            for uses_and_application in substance.uses_and_application_substances.all():
                if uses_and_application.organization and \
                        str(uses_and_application.organization.id) not in visited_organization:
                    substance_obj['organization'].append({
                        'id': uses_and_application.organization.id,
                        'name': uses_and_application.organization.name
                    })
                    visited_organization[str(uses_and_application.organization.id)] = True
            result.append(substance_obj)
        return result
