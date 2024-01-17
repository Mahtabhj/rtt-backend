from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttproduct.documents import ProductCategoryDocument, MaterialCategoryDocument, ProductDocument


class ProductCategoryOptionsApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        response = []
        organization = request.user.organization
        industry_ids = list(organization.industries.all().values_list('id', flat=True))
        product_category_queryset = ProductCategoryDocument.search().filter(
            'nested',
            path='industry',
            query=Q('terms', industry__id=industry_ids)
        )
        product_category_queryset = product_category_queryset[0:product_category_queryset.count()]

        if not product_category_queryset:
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        for product_category in product_category_queryset:
            response.append({
                'id': product_category.id,
                'name': product_category.name,
                'industries': [{'id': industry.id, 'name': industry.name} for industry in product_category.industry]
            })

        return Response(response, status=status.HTTP_200_OK)


class MaterialCategoryOptionsApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        response = []
        organization = request.user.organization
        industry_ids = list(organization.industries.all().values_list('id', flat=True))
        material_category_queryset = MaterialCategoryDocument.search().filter('terms', industry__id=industry_ids)
        material_category_queryset = material_category_queryset[0:material_category_queryset.count()]

        if not material_category_queryset:
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        for material_category in material_category_queryset:
            industry_obj = None
            if material_category.industry:
                industry_obj = {
                    'id': material_category.industry.id,
                    'name': material_category.industry.name
                }
            response.append({'id': material_category.id, 'name': material_category.name, 'industry': industry_obj})

        return Response(response, status=status.HTTP_200_OK)


class ProductOptionsApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        response = []
        product_queryset = ProductDocument.search().filter('match', organization__id=request.user.organization_id)
        product_queryset = product_queryset[0:product_queryset.count()]

        if not product_queryset:
            return Response(response, status=status.HTTP_204_NO_CONTENT)

        for product in product_queryset:
            response.append({'id': product.id, 'name': product.name})

        return Response(response, status=status.HTTP_200_OK)
