from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from elasticsearch_dsl import Q

from rttproduct.documents import ProductDocument
from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService


class ProductRelatedSubstancesApiView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule,)

    @staticmethod
    def post(request, product_id):
        limit = request.data.get('limit', 10)
        skip = request.data.get('skip', 0)
        search_keyword = request.data.get('search', None)
        organization_id = request.user.organization_id

        # checking if the product is valid or not
        product_doc_qs = ProductDocument.search().filter(
            Q('match', organization__id=organization_id) &
            Q('match', id=product_id)
        )
        if product_doc_qs.count() < 1:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        substances_data_list = []
        organization_substances_qs = RelevantSubstanceService().get_organization_relevant_substance_data(
            organization_id, data_name='product', data_id=product_id, search_keyword=search_keyword, serializer=False)
        count = organization_substances_qs.count()
        organization_substances_qs = organization_substances_qs[skip:skip + limit]

        for substance in organization_substances_qs:
            organization_substances_obj = {
                'id': substance.id,
                'name': substance.name,
                'ec_no': substance.ec_no,
                'cas_no': substance.cas_no
            }
            substances_data_list.append(organization_substances_obj)
        response = {
            'count': count,
            'results': substances_data_list
        }
        return Response(response, status=status.HTTP_200_OK)


class AllProductRelatedSubstancesIdApiView(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule,)

    @staticmethod
    def post(request, product_id):
        search_keyword = request.data.get('search', None)
        organization_id = request.user.organization_id

        # checking if the product is valid or not
        product_doc_qs = ProductDocument.search().filter(
            Q('match', organization__id=organization_id) &
            Q('match', id=product_id)
        )
        if product_doc_qs.count() < 1:
            return Response([], status=status.HTTP_204_NO_CONTENT)

        substances_id_list = []
        org_substances_doc_qs = RelevantSubstanceService().get_organization_relevant_substance_data(
            organization_id, data_name='product', data_id=product_id, search_keyword=search_keyword).source(['id'])
        org_substances_doc_qs = org_substances_doc_qs[0:org_substances_doc_qs.count()]

        for substance in org_substances_doc_qs:
            substances_id_list.append(substance.id)

        return Response(substances_id_list, status=status.HTTP_200_OK)
