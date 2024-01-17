from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttnews.documents import NewsDocument
from rttproduct.documents import ProductDocument, ProductCategoryDocument, MaterialCategoryDocument
from rttproduct.services.product_services import ProductServices
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttcore.permissions import has_substance_module_permission


class ProductListFilterOptionsApiView(APIView):
    permission_classes = (IsAuthenticated,)
    org_id = None
    product_filtered_queryset = None

    def post(self, request):
        product_categories = request.data.get('product_categories', None)
        material_categories = request.data.get('material_categories', None)
        keyword = request.data.get('keyword', None)
        from_date = request.data.get('from_date', None)
        to_date = request.data.get('to_date', None)
        response = {'product_categories': [], 'material_categories': []}
        self.org_id = request.user.organization_id

        product_queryset = ProductDocument.search().filter('match', organization__id=self.org_id)
        product_queryset = self.apply_filter(product_queryset, product_categories, material_categories, keyword, from_date, to_date)
        if not product_queryset:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        self.product_filtered_queryset = product_queryset

        for product in product_queryset:
            for product_category in product.product_categories:
                obj = self.__get_product_category_object(product_category.id, product_category.name, 'product-category')
                if obj not in response['product_categories']:
                    response['product_categories'].append(obj)
            for material_category in product.material_categories:
                obj = self.__get_material_category_object(material_category, 'material-category')
                if obj not in response['material_categories']:
                    response['material_categories'].append(obj)

        return Response(response, status=status.HTTP_200_OK)

    @staticmethod
    def apply_filter(product_search, product_categories, material_categories, keyword, from_date, to_date):
        if keyword:
            product_search = product_search.filter('match', name=keyword)
        if product_categories:
            product_search = product_search.filter(
                'nested',
                path='product_categories',
                query=Q('terms', product_categories__id=product_categories)
            )
        if material_categories:
            product_search = product_search.filter(
                'nested',
                path='material_categories',
                query=Q('terms', material_categories__id=material_categories)
            )
        if from_date and to_date:
            product_search = product_search.filter('range', last_mentioned={'gte': from_date, 'lte': to_date})
        return product_search

    def __get_product_count(self, category_id, category_type):
        product_count = 0
        if category_type == 'product-category':
            # queryset = ProductCategoryDocument.search().filter('match', id=category_id).to_queryset().first()
            # if queryset:
            #     product_count = queryset.product_product_categories.filter(organization_id=self.org_id).count()
            product_count = self.product_filtered_queryset.filter(
                'nested',
                path='product_categories',
                query=Q('match', product_categories__id=category_id)
            ).count()
        elif category_type == 'material-category':
            # queryset = MaterialCategoryDocument.search().filter('match', id=category_id).to_queryset().first()
            # if queryset:
            #     product_count = queryset.product_material_categories.filter(organization_id=self.org_id).count()
            product_count = self.product_filtered_queryset.filter(
                'nested',
                path='material_categories',
                query=Q('match', material_categories__id=category_id)
            ).count()
        return product_count

    def __get_product_category_object(self, category_id, category_name, category_type):
        return {
            'id': category_id,
            'name': category_name,
            'product_count': self.__get_product_count(category_id, category_type)
        }

    def __get_material_category_object(self, category_obj, category_type):
        return {
            'id': category_obj.id,
            'name': category_obj.name,
            'industry': {
                'id': category_obj.industry.id,
                'name': category_obj.industry.name
            },
            'product_count': self.__get_product_count(category_obj.id, category_type)
        }


class ProductsListApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        product_categories = request.data.get('product_categories', [])
        material_categories = request.data.get('material_categories', [])
        sorted_by = request.data.get('sort_by', None)
        from_date = request.data.get('from_date', None)
        to_date = request.data.get('to_date', None)
        keyword = request.data.get('keyword', None)
        organization_id = request.user.organization_id
        substance_module_permission = has_substance_module_permission(organization_id)

        queryset = ProductDocument.search()
        queryset = queryset.filter('match', organization__id=organization_id)
        if product_categories:
            queryset = queryset.filter(
                'nested',
                path='product_categories',
                query=Q('terms', product_categories__id=product_categories)
            )
        if material_categories:
            queryset = queryset.filter(
                'nested',
                path='material_categories',
                query=Q('terms', material_categories__id=material_categories)
            )
        if from_date is not None and to_date is not None:
            queryset = queryset.filter('range', last_mentioned={'gte': from_date, 'lte': to_date})
        if keyword:
            queryset = queryset.query(
                {
                    "query_string":
                        {
                         "default_field": "name",
                         "query": "*{}*".format(keyword)
                        }
                })

        # if keyword:
        #     queryset = queryset.filter(
        #         Q('match', name=keyword)
        #     )
        if sorted_by == 'last mentioned date':
            queryset = queryset.sort('-last_mentioned')
        if sorted_by == 'A > Z':
            queryset = queryset.sort('name')

        queryset = queryset[0:queryset.count()]

        result = []
        for data in queryset:
            tagged_substances_count = 0
            if substance_module_permission:
                tagged_substances_qs = RelevantSubstanceService().get_organization_relevant_substance_data(
                        organization_id, data_name='product', data_id=data.id, product_detail_page=True)
                tagged_substances_count = tagged_substances_qs.count()
            temp = {
                'id': data.id,
                'name': data.name,
                'image': data.image,
                'last_mentioned': data.last_mentioned,
                'description': data.description,
                'regulations_count': 0,
                'news_count': 0,
                'product_categories': [],
                'material_categories': [],
                'related_products': [],
                'substances_count': tagged_substances_count
            }

            product_category_ids = []
            material_category_ids = []
            for item in data.product_categories:
                temp['product_categories'].append({'id': item.id, 'name': item.name})
                product_category_ids.append(item.id)
                for value in item.product_product_categories:
                    temp_related_product = {'id': value.id, 'name': value.name}
                    if temp_related_product not in temp['related_products']:
                        temp['related_products'].append(temp_related_product)

            for item in data.material_categories:
                temp['material_categories'].append({
                    'id': item.id,
                    'name': item.name,
                    'short_name': item.short_name
                })
                material_category_ids.append(item.id)
                for value in item.product_material_categories:
                    temp_related_product = {'id': value.id, 'name': value.name}
                    if temp_related_product not in temp['related_products']:
                        temp['related_products'].append(temp_related_product)
            temp['news_count'] = self.get_news_count(product_category_ids, material_category_ids)
            temp['regulations_count'] = self.get_regulations_count(data, organization_id)
            result.append(temp)

        return Response(result, status=status.HTTP_200_OK)

    @staticmethod
    def get_regulations_count(product_queryset, organization_id):
        product_category_ids = []
        material_category_ids = [material_category.id for material_category in product_queryset.material_categories]
        for product_category in product_queryset.product_categories:
            product_category_ids.extend(ProductServices().get_all_parent_product_category_ids(product_category))
        frameworks_qs = ProductServices().get_all_frameworks(organization_id, product_category_ids,
                                                             material_category_ids)
        regulations_qs = ProductServices().get_all_regulations(organization_id, product_category_ids,
                                                               material_category_ids)
        return frameworks_qs.count() + regulations_qs.count()

    @staticmethod
    def get_news_count(product_category_ids, material_category_ids):
        news_document_queryset = NewsDocument.search().filter(Q('match', active=True) & Q('match', status='s'))
        news_document_queryset = news_document_queryset.filter(
            Q('nested',
              path='product_categories',
              query=Q('terms', product_categories__id=product_category_ids)) |
            Q('nested',
              path='material_categories',
              query=Q('terms', material_categories__id=material_category_ids))
        )
        return news_document_queryset.count()
