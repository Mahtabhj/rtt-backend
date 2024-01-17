import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.models import Substance, SubstanceUsesAndApplication
from rttproduct.models.models import Product

logger = logging.getLogger(__name__)


class SubstanceEdit(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule,)

    @staticmethod
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'uses_and_app_remove': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                  description='deleted use&app id list',
                                                  items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'uses_and_app_add': openapi.Schema(type=openapi.TYPE_ARRAY, description='added use&app id list',
                                               items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'product_remove': openapi.Schema(type=openapi.TYPE_ARRAY,
                                              description='deleted products id list',
                                              items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'product_add': openapi.Schema(type=openapi.TYPE_ARRAY, description='added products id list',
                                           items=openapi.Schema(type=openapi.TYPE_INTEGER))
        }
    ))
    def post(request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-897 --> product
        doc: https://chemycal.atlassian.net/browse/RTT-870 --> Uses&app
        """
        try:
            substance_qs = Substance.objects.filter(id=substance_id).first()
            if not substance_qs:
                return Response({"message": "Invalid substance_id"}, status=status.HTTP_400_BAD_REQUEST)
            uses_and_app_remove = request.data.get('uses_and_app_remove', None)
            uses_and_app_add = request.data.get('uses_and_app_add', None)
            product_remove = request.data.get('product_remove', None)
            product_add = request.data.get('product_add', None)

            uses_and_applications_remove_list = []
            uses_and_applications_add_list = []
            products_remove_list = []
            products_add_list = []
            organization_id = request.user.organization_id
            if uses_and_app_remove:
                uses_and_applications_remove_list = list(
                    SubstanceUsesAndApplication.objects.filter(id__in=uses_and_app_remove,
                                                               organization_id=organization_id).values_list('id',
                                                                                                            flat=True))
                substance_qs.uses_and_application_substances.remove(*uses_and_applications_remove_list)
            if uses_and_app_add:
                uses_and_applications_add_list = list(
                    SubstanceUsesAndApplication.objects.filter(id__in=uses_and_app_add,
                                                               organization_id=organization_id).values_list('id',
                                                                                                            flat=True))
                substance_qs.uses_and_application_substances.add(*uses_and_applications_add_list)
            if product_remove:
                products_remove_list = list(
                    Product.objects.filter(id__in=product_remove, organization_id=organization_id).values_list(
                        'id', flat=True))
                substance_qs.substances_product.remove(*products_remove_list)
            if product_add:
                products_add_list = list(
                    Product.objects.filter(id__in=product_add, organization_id=organization_id).values_list(
                        'id', flat=True))
                substance_qs.substances_product.add(*products_add_list)
            response = {
                'use&app': {
                    'added': uses_and_applications_add_list.__len__(),
                    'removed': uses_and_applications_remove_list.__len__()
                },
                'product': {
                    'added': products_add_list.__len__(),
                    'removed': products_remove_list.__len__()
                }

            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
