from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import copy
import logging

from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttorganization.services.organization_services import OrganizationService
from rttcore.services.id_search_service import IdSearchService
from rttproduct.services.product_services import ProductServices
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttregulation.models.models import RegulationRating, RegulatoryFrameworkRating
from rttregulation.services.region_page_services import RegionPageServices
from rttproduct.documents import ProductDocument, MaterialCategoryDocument

logger = logging.getLogger(__name__)


class RegionPageFilterOptionApiView(APIView):
    permission_classes = (IsAuthenticated,)
    region_page_service = RegionPageServices()

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'related_products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product ID',
                                               items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'product_categories': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product categories ID',
                                                 items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'material_categories': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of material categories ID',
                                                  items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'related_regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulation ID',
                                                  items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'related_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of framework ID',
                                                 items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'news': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of news ID',
                                   items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='filter by rating.'),
            'status': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of status ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of topic ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Any keyword, will be searched in task name, framework, '
                                                 'regulation name, product name')

        }
    ))
    def post(self, request, region_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1036
        """
        try:
            filters = {
                'related_products': request.data.get('related_products', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'related_regulations': request.data.get('related_regulations', None),
                'related_frameworks': request.data.get('related_frameworks', None),
                'news': request.data.get('news', None),
                'rating': request.data.get('rating', None),
                'status': request.data.get('status', None),
                'topics': request.data.get('topics', None)
            }
            region_id = int(region_id)
            top_rating = 5
            organization_id = request.user.organization_id
            search_keyword = request.data.get('search', None)
            org_service = OrganizationService()
            org_product_category_ids = org_service.get_organization_product_category_ids(organization_id)
            org_product_category_ids.sort()
            org_material_category_ids = org_service.get_organization_material_category_ids(organization_id)
            org_material_category_ids.sort()
            rel_reg_service = RelevantRegulationService()
            org_rel_regulation_ids = rel_reg_service.get_relevant_regulation_id_organization(organization_id)
            org_rel_framework_ids = rel_reg_service.get_relevant_regulatory_framework_id_organization(organization_id)

            product_categories = []
            product_cat_ids = set()
            visited_product_categories = {}

            material_cat_ids = set()
            visited_material_categories = {}

            regulations = []
            visited_regulations_in_global = {}

            regulatory_frameworks = []
            regulatory_frameworks_ids = []
            visited_regulatory_frameworks_in_global = {}

            """
            generate filter options from news_tab 
            """
            queryset_news = self.region_page_service.get_filtered_news_queryset(organization_id, region_id, filters,
                                                                                search_keyword)
            queryset_news = queryset_news[0:queryset_news.count()]
            news_top_rating_count = 0
            for news in queryset_news:
                # org tagged product_category
                self.__prepare_product_category_data(news.product_categories, org_product_category_ids,
                                                     visited_product_categories, product_categories, product_cat_ids)
                # org tagged material_categories
                self.__store_material_category_ids(news.material_categories, org_material_category_ids,
                                                   visited_material_categories, material_cat_ids)

                # org related regulations
                for regulation in news.regulations:
                    if IdSearchService().does_id_exit_in_sorted_list(org_rel_regulation_ids, regulation.id) and \
                            str(regulation.id) not in visited_regulations_in_global:
                        regulation_obj = {'id': regulation.id, 'name': regulation.name}
                        regulations.append(regulation_obj)
                        visited_regulations_in_global[str(regulation.id)] = True

                # org related framework
                for framework in news.regulatory_frameworks:
                    if IdSearchService().does_id_exit_in_sorted_list(org_rel_framework_ids, framework.id) and \
                            str(framework.id) not in visited_regulatory_frameworks_in_global:
                        framework_obj = {'id': framework.id, 'name': framework.name}
                        regulatory_frameworks.append(framework_obj)
                        visited_regulatory_frameworks_in_global[str(framework.id)] = True

                # top news rating count
                for rating in news.news_relevance:
                    if rating.relevancy == top_rating and rating.organization.id == organization_id:
                        news_top_rating_count += 1

            """
            generate filter options from regulation_tab and milestone_tab
            """
            # related_frameworks
            framework_doc_qs = self.region_page_service.get_filtered_framework_queryset(organization_id, region_id,
                                                                                        filters, search_keyword)
            framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
            regulation_top_rating_count = 0
            for framework in framework_doc_qs:
                regulatory_frameworks_ids.append(framework.id)
                if str(framework.id) not in visited_regulatory_frameworks_in_global:
                    regulatory_frameworks.append({'id': framework.id, 'name': framework.name})
                    visited_regulatory_frameworks_in_global[str(framework.id)] = True

                # top_rating count --> framework
                for framework_rating in framework.regulatory_framework_rating:
                    if framework_rating.rating == top_rating and framework_rating.organization.id == organization_id:
                        regulation_top_rating_count += 1
                # org tagged product_category
                self.__prepare_product_category_data(framework.product_categories, org_product_category_ids,
                                                     visited_product_categories, product_categories, product_cat_ids)

                # org tagged material_categories
                self.__store_material_category_ids(framework.material_categories, org_material_category_ids,
                                                   visited_material_categories, material_cat_ids)

            # related regulations
            regulation_filters = copy.deepcopy(filters)
            if not filters.get('related_frameworks', None):
                regulation_filters['related_frameworks'] = []
            regulation_filters['related_frameworks'].extend(regulatory_frameworks_ids)
            regulation_doc_qs = self.region_page_service.get_filtered_regulation_queryset(
                organization_id, region_id, regulation_filters, search_keyword)
            regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
            for regulation in regulation_doc_qs:
                if str(regulation.id) not in visited_regulations_in_global:
                    regulation_obj = {'id': regulation.id, 'name': regulation.name}
                    regulations.append(regulation_obj)
                    visited_regulations_in_global[str(regulation.id)] = True

                # top rating count --> regulation
                for regulation_rating in regulation.regulation_rating:
                    if regulation_rating.rating == top_rating and \
                            regulation_rating.organization.id == organization_id:
                        regulation_top_rating_count += 1

                # org tagged product_category
                self.__prepare_product_category_data(regulation.product_categories, org_product_category_ids,
                                                     visited_product_categories, product_categories,
                                                     product_cat_ids)

                # org tagged material_categories
                self.__store_material_category_ids(regulation.material_categories, org_material_category_ids,
                                                   visited_material_categories, material_cat_ids)

            # prepare material_category with industry data
            material_cat_ids = list(material_cat_ids)
            material_categories = self.get_related_material_cat_data(material_cat_ids)

            # generating related_products from product_cat, mat_cat which are collected from three tabs and region_id
            product_cat_ids = list(product_cat_ids)
            related_products = self.get_related_products_data(product_cat_ids, material_cat_ids, organization_id,
                                                              filters)

            response = {
                'products': {
                    'length': related_products.__len__(),  # related_products count()
                    'filtered_items_length': product_categories.__len__(),  # product_categories count()
                    'categories': {
                        'product_categories': {'title': 'Product categories', 'options': product_categories},
                        'related_products': {'title': 'Related products', 'options': related_products}
                    }
                },
                'material': {
                    'length': material_categories.__len__(),  # material_categories count()
                    'categories': {
                        'material_categories': {'title': 'Material categories', 'options': material_categories}
                    }
                },
                'regulations': {
                    'length': regulatory_frameworks.__len__() + regulations.__len__(),
                    # regulatory_frameworks count() + regulations count()
                    'filtered_items_length': 0,
                    'categories': {
                        'related_frameworks': {'title': 'Related frameworks', 'options': regulatory_frameworks},
                        'related_regulations': {'title': 'Related regulations', 'options': regulations}
                    },
                },
                'ratings': {
                    'length': news_top_rating_count + regulation_top_rating_count,
                }
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def has_top_rating(organization_id, rating_val, data_name, data_id):
        if data_name == 'regulation':
            return RegulationRating.objects.filter(rating=rating_val, regulation_id=data_id,
                                                   organization_id=organization_id).exists()
        else:
            return RegulatoryFrameworkRating.objects.filter(rating=rating_val, regulatory_framework_id=data_id,
                                                            organization_id=organization_id).exists()

    @staticmethod
    def __prepare_product_category_data(product_cat_queryset, org_product_category_ids, visited_product_categories,
                                        product_categories, product_cat_ids):
        # org tagged product_category
        for product_category in product_cat_queryset:
            if IdSearchService().does_id_exit_in_sorted_list(org_product_category_ids,
                                                             product_category.id) \
                    and str(product_category.id) not in visited_product_categories:
                product_cat_obj = {'id': product_category.id, 'name': product_category.name}
                product_categories.append(product_cat_obj)
                # store product_cat to generate related_products
                product_cat_ids.add(product_category.id)
                visited_product_categories[str(product_category.id)] = True

    @staticmethod
    def __store_material_category_ids(material_cat_queryset, org_material_category_ids, visited_material_categories,
                                      material_cat_ids):
        # org tagged material_categories
        for material_category in material_cat_queryset:
            if IdSearchService().does_id_exit_in_sorted_list(org_material_category_ids, material_category.id) \
                    and str(material_category.id) not in visited_material_categories:
                material_cat_ids.add(material_category.id)
                visited_material_categories[str(material_category.id)] = True

    @staticmethod
    def get_related_material_cat_data(material_cat_ids):
        result = []
        material_category_doc_qs: MaterialCategoryDocument = MaterialCategoryDocument.search().filter(
            Q('terms', id=material_cat_ids)
        ).source(['id', 'name', 'industry'])
        material_category_doc_qs = material_category_doc_qs[0:material_category_doc_qs.count()]
        for material_cat in material_category_doc_qs:
            result.append({
                'id': material_cat.id,
                'name': material_cat.name,
                'industry': {
                    'id': material_cat.industry.id,
                    'name': material_cat.industry.name
                }
            })
        return result

    @staticmethod
    def get_related_products_data(product_cat_ids, material_cat_ids, organization_id, filters):
        result = []
        if not filters.get('product_categories', None):
            filters['product_categories'] = []
        filters['product_categories'].extend(product_cat_ids)
        filters['product_categories'] = ProductServices().get_all_tree_child_product_category_ids(
            filters['product_categories'])

        if not filters.get('material_categories', None):
            filters['material_categories'] = []
        filters['material_categories'].extend(material_cat_ids)

        product_doc_qs: ProductDocument = ProductDocument.search().filter('match', organization__id=organization_id)
        filters['topics'] = None
        related_product_qs = ProductServices().get_related_product_filtered_queryset(filters, product_doc_qs)
        related_product_qs = related_product_qs[0:related_product_qs.count()]
        for product in related_product_qs:
            result.append({
                'id': product.id,
                'name': product.name
            })
        return result
