import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService

logger = logging.getLogger(__name__)


class ProductDetailsRelSubstance(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule,)

    @staticmethod
    def post(request, product_id, *args, **kwargs):
        try:
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            search_keyword = request.data.get('search', None)
            organization_id = request.user.organization_id

            substances_list = []
            substances_doc_qs = RelevantSubstanceService().get_organization_relevant_substance_data(
                organization_id, data_name='product', data_id=product_id, search_keyword=search_keyword,
                serializer=False, product_detail_page=True)
            queryset_count = substances_doc_qs.count()
            substances_doc_qs = substances_doc_qs[skip:skip + limit]

            for substance in substances_doc_qs:
                substance_obj = {
                    'id': substance.id,
                    'name': substance.name,
                    'ec_no': substance.ec_no,
                    'cas_no': substance.cas_no,
                    'uses_and_application': [{'id': use_and_app.id, 'name': use_and_app.name}
                                             for use_and_app in substance.uses_and_application_substances
                                             if use_and_app.organization.id == organization_id]
                }
                substances_list.append(substance_obj)
            response = {
                'count': queryset_count,
                'results': substances_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)