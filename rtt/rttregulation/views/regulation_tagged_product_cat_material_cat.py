import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from rttregulation.models.models import ProductCategory, MaterialCategory

logger = logging.getLogger(__name__)


class RegulationTaggedProductCatMaterialCatAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulation ID',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of framework ID',
                                         items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        }
    ))
    def post(request, *args, **kwargs):
        try:
            regulations = request.data.get('regulations', None)
            frameworks = request.data.get('frameworks', None)
            reg_list = []
            fw_list = []
            if regulations:
                reg_list = regulations
            if frameworks:
                fw_list = frameworks

            product_category_id_list = ProductCategory.objects.filter(
                Q(product_cat_reg_framework__id__in=fw_list) | Q(regulation_product_categories__id__in=reg_list)
            ).values_list('id', flat=True).distinct()

            material_category_id_list = MaterialCategory.objects.filter(
                Q(material_cat_reg_framework__id__in=fw_list) | Q(regulation_material_categories__id__in=reg_list)
            ).values_list('id', flat=True).distinct()

            response = {
                'product_categories': list(product_category_id_list),
                'material_categories': list(material_category_id_list),
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
