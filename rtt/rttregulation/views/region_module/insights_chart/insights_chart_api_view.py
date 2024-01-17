from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Q

import copy
import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttregulation.services.region_page_services import RegionPageServices
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.services.relevant_regulation_service import RelevantRegulationService

logger = logging.getLogger(__name__)


class InsightsChartApiView(APIView):
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
            'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='filter by rating.'),
            'status': openapi.Schema(type=openapi.TYPE_ARRAY, description='filter by status.',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of topic ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Any keyword, will be searched in task name, framework, '
                                                 'regulation name, product name'),
            'news_tab': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='If the news tab is selected, news_tab '
                                                                              'will be true.'),
            'regulation_tab': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='If the regulation tab is selected,'
                                                                                    'regulation_tab will be true.'),
            'milestone_tab': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='If the milestone tab is selected,'
                                                                                   ' milestone_tab will be true.')

        }
    ))
    def post(self, request, region_id):
        """
        Docs: https://chemycal.atlassian.net/browse/RTT-1041
        """
        try:
            filters = {
                'related_products': request.data.get('related_products', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'related_regulations': request.data.get('related_regulations', None),
                'related_frameworks': request.data.get('related_frameworks', None),
                'rating': request.data.get('rating', None),
                'status': request.data.get('status', None),
                'topics': request.data.get('topics', None)
            }
            region_id = int(region_id)
            organization_id = request.user.organization_id
            search_keyword = request.data.get('search', None)

            product_categories = []
            visited_product_categories = {}

            material_categories = []
            visited_material_categories = {}

            news_tab = request.data.get('news_tab', False)
            regulations_tab = request.data.get('regulation_tab', False)
            milestone_tab = request.data.get('milestone_tab', False)

            tab_request_count = 0
            if news_tab:
                tab_request_count += 1
            if regulations_tab:
                tab_request_count += 1
            if milestone_tab:
                tab_request_count += 1
            if tab_request_count != 1:
                return Response({"message": "One and only one tab will be true"}, status=status.HTTP_400_BAD_REQUEST)

            """
            Data for news tab
            """
            if news_tab:
                queryset_news = self.region_page_service.get_filtered_news_queryset(organization_id, region_id, filters,
                                                                                    search_keyword)
                queryset_news = queryset_news[0:queryset_news.count()]

                for news in queryset_news:
                    # org tagged product_category
                    product_category_qs = CategoryValidatorServices().get_relevant_product_categories(
                        organization_id, news.product_categories)
                    self.prepare_data(product_category_qs, product_categories, visited_product_categories,
                                      'product_categories', 'news', news.id, True)

                    # org tagged material_categories
                    material_categories_qs = CategoryValidatorServices().get_relevant_material_categories(
                        organization_id, news.material_categories)
                    self.prepare_data(material_categories_qs, material_categories, visited_material_categories,
                                      'material_categories', 'news', news.id, True)

            """
            Data for regulation tab OR Data via milestone
            """
            if regulations_tab or milestone_tab:
                framework_ids = []
                # generate filter from framework
                framework_doc_qs = self.region_page_service.get_filtered_framework_queryset(
                    organization_id, region_id, filters, search_keyword)
                related_milestones_ids = RelevantRegulationService().get_relevant_milestone_id_organization(
                    organization_id)
                if milestone_tab:
                    framework_doc_qs = framework_doc_qs.filter(
                        # making sure every framework has milestone(s)
                        Q('nested',
                          path='regulatory_framework_milestone',
                          query=Q('exists', field="regulatory_framework_milestone.id")) &
                        Q('nested',
                          path='regulatory_framework_milestone',
                          query=Q('terms', regulatory_framework_milestone__id=related_milestones_ids))
                    )
                framework_doc_qs = framework_doc_qs[0:framework_doc_qs.count()]
                for framework in framework_doc_qs:
                    framework_ids.append(framework.id)
                    # org tagged product_category
                    product_category_qs = CategoryValidatorServices().get_relevant_product_categories(
                        organization_id, framework.product_categories)
                    self.prepare_data(product_category_qs, product_categories, visited_product_categories,
                                      'product_categories', 'frameworks', framework.id)

                    # org tagged material_categories
                    material_categories_qs = CategoryValidatorServices().get_relevant_material_categories(
                        organization_id, framework.material_categories)
                    self.prepare_data(material_categories_qs, material_categories, visited_material_categories,
                                      'material_categories', 'frameworks', framework.id)
                # generate filter from regulation
                regulation_filters = copy.deepcopy(filters)
                if not filters.get('related_frameworks', None):
                    regulation_filters['related_frameworks'] = []
                regulation_filters['related_frameworks'].extend(framework_ids)
                queryset_regulation = self.region_page_service.get_filtered_regulation_queryset(
                    organization_id, region_id, regulation_filters, search_keyword)
                if milestone_tab:
                    queryset_regulation = queryset_regulation.filter(
                        # making sure every regulation has milestone(s)
                        Q('nested',
                          path='regulation_milestone',
                          query=Q('exists', field="regulation_milestone.id")) &
                        Q('nested',
                          path='regulation_milestone',
                          query=Q('terms', regulation_milestone__id=related_milestones_ids))
                    )
                queryset_regulation = queryset_regulation[0:queryset_regulation.count()]

                for regulation in queryset_regulation:
                    # org tagged product_category
                    product_category_qs = CategoryValidatorServices().get_relevant_product_categories(
                        organization_id, regulation.product_categories)
                    self.prepare_data(product_category_qs, product_categories, visited_product_categories,
                                      'product_categories', 'regulations', regulation.id)

                    # org tagged material_categories
                    material_categories_qs = CategoryValidatorServices().get_relevant_material_categories(
                        organization_id, regulation.material_categories)
                    self.prepare_data(material_categories_qs, material_categories, visited_material_categories,
                                      'material_categories', 'regulations', regulation.id)

            response = {'product_categories': product_categories, 'material_categories': material_categories}
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def prepare_data(queryset, result_data, visited_result_data, queryset_type, are_type, selected_are_type_id,
                     only_news=False):
        """
        queryset: either product_categories or material_cat
        result_data: will be stored queryset_obj here
        visited_result_data: dict where data will be saved which are already visited
        queryset_type: string --> either product_categories or material_categories
        are_type: string --> news, regulations or frameworks
        selected_are_type_id:
        """
        for data in queryset:
            if str(data.id) in visited_result_data:
                idx = visited_result_data[str(data.id)]
                result_data[idx][are_type]['selected_ids'].append(selected_are_type_id)
                result_data[idx][are_type]['total_length'] += 1
            else:
                filters_for_total_len = {
                    'product_categories': [],
                    'material_categories': [],
                }

                if queryset_type == 'product_categories':
                    filters_for_total_len['product_categories'].append(data.id)
                elif queryset_type == 'material_categories':
                    filters_for_total_len['material_categories'].append(data.id)

                data_obj = {
                    'id': data.id,
                    'title': data.name
                }
                if only_news:
                    data_obj['news'] = {
                        'total_length': 0,
                        'selected_ids': []
                    }
                else:
                    data_obj['regulations'] = {
                        'total_length': 0,
                        'selected_ids': []
                    }
                    data_obj['frameworks'] = {
                        'total_length': 0,
                        'selected_ids': []
                    }
                data_obj[are_type]['selected_ids'].append(selected_are_type_id)
                data_obj[are_type]['total_length'] += 1
                visited_result_data[str(data.id)] = len(result_data)
                if queryset_type == 'material_categories':
                    data_obj['industry'] = {
                        'id': data.industry.id,
                        'name': data.industry.name
                    }
                result_data.append(data_obj)
