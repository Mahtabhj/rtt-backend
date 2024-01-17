import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttproduct.models.core_models import Industry
from rttproduct.filters import ProductCategoryFilter
from rttproduct.models.models import Product, ProductCategory, MaterialCategory
from rttproduct.serializers import serializers

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    serializer_classes = {
        'update': serializers.ProductUpdateSerializer,
        'partial_update': serializers.ProductUpdateSerializer,
    }
    default_serializer_class = serializers.ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request):
        data = request.data.copy()
        data['organization'] = request.user.organization_id
        serializer = serializers.ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            flag = False
            if not request.data.get('material_categories', None):
                instance.material_categories.clear()
                flag = True
            if not request.data.get('product_categories', None):
                instance.product_categories.clear()
                flag = True
            if not request.data.get('substance_use_and_apps', None):
                instance.substance_use_and_apps.clear()
                flag = True
            if flag:
                instance.save()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='product-category-material-category-add-remove')
    def product_category_material_category_add_remove(self, request, pk, *args, **kwargs):
        try:
            # list of product_categories ID
            product_categories = request.data.get('product_categories', None)
            # list of material_categories ID
            material_categories = request.data.get('material_categories', None)
            if not product_categories and not material_categories:
                return Response({"message": "product_categories OR material_categories must be sent"},
                                status=status.HTTP_400_BAD_REQUEST)

            # on which field operation will be done
            field = request.data.get('field', None)
            if not field or field not in ['product_categories', 'material_categories']:
                return Response({"message": "field must be product_categories OR material_categories"},
                                status=status.HTTP_400_BAD_REQUEST)

            # operation_action is either add or remove
            operation_action = request.data.get('action', None)
            if not operation_action or operation_action not in ['add', 'remove']:
                return Response({"message": "action must be add OR remove sent"}, status=status.HTTP_400_BAD_REQUEST)

            instance = Product.objects.get(id=pk)

            if operation_action.lower() == 'add':
                if product_categories:
                    instance.product_categories.add(*product_categories)
                if material_categories:
                    instance.material_categories.add(*material_categories)
            else:
                if product_categories:
                    instance.product_categories.remove(*product_categories)
                if material_categories:
                    instance.material_categories.remove(*material_categories)

            return Response({"message": f"{field} {operation_action} success."}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='product-related-substance-add-remove')
    def product_related_substance_add_remove(self, request, pk, *args, **kwargs):
        try:
            substances = request.data.get('substances', None)
            if not substances:
                return Response({"message": "substances must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            action = request.data.get('action', None)
            if not action:
                return Response({"message": "action must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            instance = Product.objects.get(id=pk)
            if action.lower() == 'add':
                instance.substances.add(*substances)
            else:
                instance.substances.remove(*substances)
            return Response({"message": f"substances {action} success"}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            organization_id = request.user.organization_id
            instance = self.get_object()
            if instance.organization.id != organization_id:
                return Response({"message": "Don't have the permission to delete"}, status=status.HTTP_401_UNAUTHORIZED)
            self.perform_destroy(instance)
            return Response({"message": "The product has been deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industry.objects.all().prefetch_related('product_category_industries', 'material_category_industry')
    serializer_class = serializers.IndustrySerializer
    permission_classes = (IsAuthenticated,)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all().select_related('parent').prefetch_related('industry')
    serializer_class = serializers.ProductCategorySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = ProductCategoryFilter
    search_fields = ['name']
    filterset_fields = ['industry']
    permission_classes = (IsAuthenticated,)


class MaterialCategoryViewSet(viewsets.ModelViewSet):
    queryset = MaterialCategory.objects.all().select_related('industry')
    permission_classes = (IsAuthenticated,)
    serializer_classes = {
        'list': serializers.MaterialCategoryDetailsSerializer,
    }
    default_serializer_class = serializers.MaterialCategorySerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
