from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttregulation.services.rating_search_service import RatingSearchService
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttcore.permissions import IsActiveSubstanceModule

logger = logging.getLogger(__name__)


class RelSubstanceDataInsideOtherDetailsAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule,)
    rating_service = RatingSearchService()

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'is_framework': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true if data is framework',),
            'is_regulation': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true if data is regulation',),
            'is_milestone': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true if data is milestone',),
            'is_news': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='true if data is news',),
            'only_my_org': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                          description='Default False , True if only my organization substances'),
            'search': openapi.Schema(type=openapi.TYPE_STRING, description='Search in substance name , ec and cas')
        }
    ))
    def post(self, request, data_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1111?focusedCommentId=13172
        """
        try:
            organization_id = request.user.organization_id
            data_name = None
            count = 0

            if request.data.get('is_framework', False):
                data_name = 'framework'
                count += 1
            if request.data.get('is_regulation', False):
                data_name = 'regulation'
                count += 1
            if request.data.get('is_milestone', False):
                data_name = 'milestone'
                count += 1
            if request.data.get('is_news', False):
                data_name = 'news'
                count += 1

            if count != 1:
                return Response({"message": "Only Framework/Regulation/Milestone/News can be selected"},
                                status=status.HTTP_400_BAD_REQUEST)

            only_my_org = request.data.get('only_my_org', False)
            search_keyword = request.data.get('search', None)

            substances_doc_qs = RelevantSubstanceService().get_organization_relevant_substance_data(
                organization_id, data_name=data_name, data_id=data_id, search_keyword=search_keyword,
                serializer=False, only_my_org=only_my_org)
            substances_doc_qs = substances_doc_qs[0:substances_doc_qs.count()]
            response = []
            for substance in substances_doc_qs:
                substance_data = self.get_substance_data(substance, organization_id)
                response.append(substance_data)

            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_substance_data(substance, organization_id):
        is_relevant = False
        uses_and_applications_list = []
        for use_and_application in substance.uses_and_application_substances:
            if use_and_application.organization.id == organization_id:
                use_and_application_obj = {
                    'id': use_and_application.id,
                    'name': use_and_application.name,
                }
                uses_and_applications_list.append(use_and_application_obj)
                is_relevant = True

        substance_data = {
            'id': substance.id,
            'name': substance.name,
            'ec_no': substance.ec_no,
            'cas_no': substance.cas_no,
            'uses_and_applications': uses_and_applications_list,
            'is_relevant': is_relevant
        }
        return substance_data
