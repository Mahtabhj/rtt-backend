from datetime import datetime

import pytz
from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.permissions import has_substance_module_permission
from rttcore.services.dashboard_services import DashboardService
from rttcore.services.id_search_service import IdSearchService
from rttnews.documents import RegionDocument, NewsDocument
from rttnews.serializers.serializers import NewsCategoryIdNameSerializer
from rttorganization.services.organization_services import OrganizationService
from rttproduct.documents import MaterialCategoryDocument, ProductCategoryDocument
from rttproduct.serializers.serializers import ProductCategoryIdNameSerializer, \
    MaterialCategoryIdNameShortNameSerializer
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.documents import RegulatoryFrameworkDocument, RegulationDocument, TopicDocument
from rttregulation.serializers.serializers import RegionIdNameSerializer, TopicIdNameSerializer
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttregulation.services.relevant_topic_service import RelevantTopicService

utc = pytz.UTC


class DashboardRightChartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            filters = {
                'topics': request.data.get('topics', None),
                'regions': request.data.get('regions', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None),
                'related_products': request.data.get('related_products', None),
                'related_regulations': request.data.get('related_regulations', None),
                'related_frameworks': request.data.get('related_frameworks', None),
                'news': request.data.get('news', None),
                'regulations': request.data.get('regulations', None),
                'frameworks': request.data.get('frameworks', None),
            }
            region_results = []
            material_cat_results = []
            product_cat_results = []
            organization_id = request.user.organization_id

            filters_value_for_total_len = {
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None),
                'organization_id': organization_id,
            }

            dashboard_service = DashboardService()

            queryset_news = []
            queryset_regulation = []
            queryset_regulatory = []

            if dashboard_service.is_return_data(filters, 'news'):
                queryset_news = dashboard_service.get_filtered_news_queryset(filters, organization_id)
                queryset_news = queryset_news[0:queryset_news.count()]

            if dashboard_service.is_return_data(filters, 'regulations'):
                queryset_regulation = dashboard_service.get_filtered_regulation_queryset(filters, organization_id)
                queryset_regulation = queryset_regulation[0:queryset_regulation.count()]

            if dashboard_service.is_return_data(filters, 'frameworks'):
                queryset_regulatory = dashboard_service.get_filtered_regulatory_framework_queryset(filters,
                                                                                                   organization_id)
                queryset_regulatory = queryset_regulatory[0:queryset_regulatory.count()]

            for news in queryset_news:
                self.prepare_data(news.regions, region_results, 'news', news.id, filters_value_for_total_len, 'regions')
                self.prepare_data(CategoryValidatorServices().get_relevant_product_categories(
                    organization_id, news.product_categories),
                    product_cat_results, 'news', news.id, filters_value_for_total_len, 'product_categories')
                self.prepare_data(CategoryValidatorServices().get_relevant_material_categories(
                    organization_id, news.material_categories),
                    material_cat_results, 'news', news.id, filters_value_for_total_len, 'material_categories')

            for regulation in queryset_regulation:
                self.prepare_data(regulation.regulatory_framework.regions, region_results, 'regulations', regulation.id,
                                  filters_value_for_total_len, 'regions')
                self.prepare_data(CategoryValidatorServices().get_relevant_product_categories(
                    organization_id, regulation.product_categories),
                    product_cat_results, 'regulations', regulation.id, filters_value_for_total_len, 'product_categories')
                self.prepare_data(CategoryValidatorServices().get_relevant_material_categories(
                    organization_id, regulation.material_categories), material_cat_results, 'regulations',
                    regulation.id, filters_value_for_total_len, 'material_categories')

            for regulatory in queryset_regulatory:
                self.prepare_data(regulatory.regions, region_results, 'frameworks', regulatory.id,
                                  filters_value_for_total_len, 'regions')
                self.prepare_data(CategoryValidatorServices().get_relevant_product_categories(
                    organization_id, regulatory.product_categories),
                    product_cat_results, 'frameworks', regulatory.id, filters_value_for_total_len, 'product_categories')
                self.prepare_data(CategoryValidatorServices().get_relevant_material_categories(
                    organization_id, regulatory.material_categories), material_cat_results,
                    'frameworks', regulatory.id, filters_value_for_total_len, 'material_categories')

            return Response(
                {'regions': region_results, 'material': material_cat_results, 'product': product_cat_results},
                status=status.HTTP_200_OK)
        except Exception as ex:
            is_es_rebuild = DashboardService().check_es_exception(ex)
            return self.post(request) if is_es_rebuild \
                else Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def is_id_exists_in_list(list_data, id):
        """
        Return found and index.
        """
        for index, item in enumerate(list_data):
            if item['id'] == id:
                return True, index
        return False, -1

    def prepare_data(self, source_data, result_data, area, area_selected_id, filters_value_for_total_len, filters_name):
        for data in source_data:
            found, index = self.is_id_exists_in_list(result_data, data.id)
            if found:
                result_data[index][area]['selected_ids'].append(area_selected_id)
            else:
                filters_total_len = {
                    'from_date': filters_value_for_total_len['from_date'],
                    'to_date': filters_value_for_total_len['to_date'],
                    'regions': [],
                    'product_categories': [],
                    'material_categories': [],
                }
                queryset_news_total_len = 0
                queryset_regulation_total_len = 0
                queryset_regulatory_total_len = 0

                dashboard_service = DashboardService()

                if filters_name == 'regions':
                    filters_total_len['regions'].append(data.id)
                elif filters_name == 'product_categories':
                    filters_total_len['product_categories'].append(data.id)
                elif filters_name == 'material_categories':
                    filters_total_len['material_categories'].append(data.id)

                queryset_news_total_len = dashboard_service.get_filtered_news_queryset(
                    filters_total_len, filters_value_for_total_len['organization_id']).count()
                queryset_regulation_total_len = dashboard_service.get_filtered_regulation_queryset(
                    filters_total_len, filters_value_for_total_len['organization_id']).count()
                queryset_regulatory_total_len = dashboard_service.get_filtered_regulatory_framework_queryset(
                    filters_total_len, filters_value_for_total_len['organization_id']).count()

                temp = {
                    'id': data.id,
                    'title': data.name,
                    'news': {
                        'total_length': queryset_news_total_len,
                        'selected_ids': []
                    },
                    'regulations': {
                        'total_length': queryset_regulation_total_len,
                        'selected_ids': []
                    },
                    'frameworks': {
                        'total_length': queryset_regulatory_total_len,
                        'selected_ids': []
                    }
                }
                temp[area]['selected_ids'].append(area_selected_id)
                if filters_name == 'material_categories':
                    temp['industry'] = {
                        'id': data.industry.id,
                        'name': data.industry.name
                    }
                result_data.append(temp)


class DashboardContentApiView(APIView):
    permission_classes = [IsAuthenticated]
    rating_search_service = RatingSearchService()

    def post(self, request):
        try:
            filters = {
                'topics': request.data.get('topics', None),
                'regions': request.data.get('regions', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'from_date': request.data.get('from', None),
                'to_date': request.data.get('to', None),
                'news': request.data.get('news', None),
                'regulations': request.data.get('regulations', None),
                'frameworks': request.data.get('frameworks', None),
                'related_products': request.data.get('related_products', None),
                'related_regulations': request.data.get('related_regulations', None),
                'related_frameworks': request.data.get('related_frameworks', None),
            }
            from_date = datetime.strptime(filters['from_date'], "%Y-%m-%d").replace(tzinfo=utc) if filters[
                'from_date'] else None
            to_date = datetime.strptime(filters['to_date'], "%Y-%m-%d").replace(tzinfo=utc, hour=23) if filters[
                'to_date'] else None
            self.organization_id = request.user.organization_id
            substance_module_permission = has_substance_module_permission(self.organization_id)
            response = []
            dashboard_service = DashboardService()

            queryset_news = dashboard_service.get_filtered_news_queryset(filters, self.organization_id).sort(
                '-pub_date')
            queryset_news = queryset_news[0:queryset_news.count()]

            queryset_regulation = dashboard_service.get_filtered_regulation_queryset(filters,
                                                                                     self.organization_id).sort(
                '-regulation_milestone.from_date')
            queryset_regulation = queryset_regulation[0:queryset_regulation.count()]

            queryset_regulatory = dashboard_service.get_filtered_regulatory_framework_queryset(filters,
                                                                                               self.organization_id).sort(
                '-regulatory_framework_milestone.from_date')
            queryset_regulatory = queryset_regulatory[0:queryset_regulatory.count()]

            """
            news data
            """
            if dashboard_service.is_return_data(filters, 'news'):
                relevant_regulation_ids_organization = RelevantRegulationService(). \
                    get_relevant_regulation_id_organization(self.organization_id)
                relevant_regulatory_framework_ids_organization = RelevantRegulationService(). \
                    get_relevant_regulatory_framework_id_organization(self.organization_id)
                for news in queryset_news:
                    news_rating_obj = self.rating_search_service.get_news_rating_obj(self.organization_id, news.id,
                                                                                     news.news_relevance)
                    news_data = {
                        'type': 'news',
                        'id': news.id,
                        'date': news.pub_date,
                        'regions': RegionIdNameSerializer(news.regions, many=True).data,
                        'status': 'New' if news.status == 'n' else 'Selected' if news.status == 's' else 'Discharged',
                        'source': {'image': news.source.image, 'name': news.source.name},
                        'title': news.title,
                        'body': news.body,
                        'impact_rating': news_rating_obj,
                        'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                            self.organization_id,
                            news.product_categories, serialize=True),
                        'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                            self.organization_id,
                            news.material_categories, serialize=True),
                        'regulations': [],
                        'frameworks': [],
                        'topics': [],
                        'substances': RelevantSubstanceService().get_organization_relevant_substance_data(
                            self.organization_id, data_name='news', data_id=news.id, serializer=True) if
                        substance_module_permission else []
                    }
                    for news_category in news.news_categories:
                        if news_category.topic:
                            topic_obj = {
                                'id': news_category.topic.id,
                                'name': news_category.topic.name
                            }
                            if topic_obj not in news_data['topics']:
                                news_data['topics'].append(topic_obj)

                    relevant_regulation = list(filter(lambda rel_regulation:
                                                      rel_regulation.id in relevant_regulation_ids_organization,
                                                      news.regulations))
                    for regulation in relevant_regulation:
                        regulation_rating_obj = self.rating_search_service.get_regulation_rating_obj(self.organization_id,
                                                                                                     regulation.id)
                        if regulation.review_status == 'o':
                            news_data['regulations'].append({
                                'id': regulation.id,
                                'name': regulation.name,
                                'type': regulation.type.name,
                                'status': regulation.status.name,
                                'date': regulation.created,
                                'description': regulation.description,
                                'impact_rating': regulation_rating_obj,
                                'regions': RegionIdNameSerializer(regulation.regulatory_framework.regions,
                                                                  many=True).data,
                            })
                    relevant_regulatory_framework = list(filter(lambda rel_reg_fw:
                                                                rel_reg_fw.id in
                                                                relevant_regulatory_framework_ids_organization,
                                                                news.regulatory_frameworks))
                    for framework in relevant_regulatory_framework:
                        framework_rating_obj = self.rating_search_service.get_framework_rating_obj(self.organization_id,
                                                                                                   framework.id)
                        if framework.review_status == 'o':
                            news_data['frameworks'].append({
                                'id': framework.id,
                                'name': framework.name,
                                'status': framework.status.name,
                                'date': framework.created,
                                'description': framework.description,
                                'impact_rating': framework_rating_obj,
                                'regions': RegionIdNameSerializer(framework.regions, many=True).data,
                            })

                    response.append(news_data)

            """
            regulatory-framework data
            """
            if dashboard_service.is_return_data(filters, 'frameworks'):
                rel_reg_ids = RelevantRegulationService().get_relevant_regulation_id_organization(self.organization_id)
                for regulatory in queryset_regulatory:
                    if regulatory.review_status == 'o':
                        rf_rating_obj = self.rating_search_service.get_framework_rating_obj(self.organization_id,
                                                                                            regulatory.id,
                                                                                            regulatory.regulatory_framework_rating)
                        framework_data = self.__get_regulatory_framework_formatted_data(regulatory, rf_rating_obj,
                                                                                        substance_module_permission,
                                                                                        rel_reg_ids)
                        for milestone in regulatory.regulatory_framework_milestone:
                            if from_date and to_date:
                                if from_date <= milestone.from_date <= to_date:
                                    framework_data['date'] = milestone.from_date
                                    framework_data['milestones'] = [{
                                        'id': milestone.id,
                                        'name': milestone.name,
                                        'type': milestone.type.name,
                                        'description': milestone.description,
                                        'date': milestone.from_date,
                                    }]
                                else:
                                    continue
                            else:
                                framework_data['date'] = milestone.from_date
                                framework_data['milestones'] = [{
                                    'id': milestone.id,
                                    'name': milestone.name,
                                    'type': milestone.type.name,
                                    'description': milestone.description,
                                    'date': milestone.from_date,
                                }]
                            response.append(framework_data.copy())
            """
            regulation data
            """
            if dashboard_service.is_return_data(filters, 'regulations'):
                for regulation in queryset_regulation:
                    regulation_rating_obj = self.rating_search_service.get_regulation_rating_obj(self.organization_id,
                                                                                                 regulation.id,
                                                                                                 regulation.regulation_rating)
                    if regulation.review_status == 'o':
                        regulation_data = self.__get_regulation_formatted_data(regulation, regulation_rating_obj,
                                                                               substance_module_permission)
                        for milestone in regulation.regulation_milestone:
                            if from_date and to_date:
                                if milestone.from_date and from_date <= milestone.from_date <= to_date:
                                    regulation_data['date'] = milestone.from_date
                                    regulation_data['milestones'] = [{
                                        'id': milestone.id,
                                        'name': milestone.name,
                                        'type': milestone.type.name,
                                        'description': milestone.description,
                                        'date': milestone.from_date
                                    }]
                                else:
                                    continue
                            else:
                                regulation_data['date'] = milestone.from_date
                                regulation_data['milestones'] = [{
                                    'id': milestone.id,
                                    'name': milestone.name,
                                    'type': milestone.type.name,
                                    'description': milestone.description,
                                    'date': milestone.from_date
                                }]

                            response.append(regulation_data.copy())

            response.sort(key=lambda data: data['date'], reverse=True)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            is_es_rebuild = DashboardService().check_es_exception(ex)
            return self.post(request) if is_es_rebuild \
                else Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def __get_regulatory_framework_formatted_data(self, regulatory, rf_rating_obj, substance_module_permission,
                                                  rel_reg_ids):
        framework_data = {
            'type': 'regulatory-framework',
            'id': regulatory.id,
            'date': None,
            'status': regulatory.status.name,
            'issuing_body': {'id': regulatory.issuing_body.id, 'name': regulatory.issuing_body.name},
            'name': regulatory.name,
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(self.organization_id,
                                                                                              regulatory.product_categories,
                                                                                              serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(self.organization_id,
                                                                                                regulatory.material_categories,
                                                                                                serialize=True),
            'regulations': [],
            'milestones': [],
            'regions': RegionIdNameSerializer(regulatory.regions, many=True).data,
            'impact_rating': rf_rating_obj,
            'topics': TopicIdNameSerializer(regulatory.topics, many=True).data,
            'substances': RelevantSubstanceService().get_organization_relevant_substance_data(
                self.organization_id, data_name='framework', data_id=regulatory.id, serializer=True)
            if substance_module_permission else []
        }

        for regulations in regulatory.regulation_regulatory_framework:
            if regulations.review_status == 'o' and IdSearchService().does_id_exit_in_sorted_list(rel_reg_ids,
                                                                                                  regulations.id):
                framework_data['regulations'].append({
                    'id': regulations.id,
                    'name': regulations.name,
                    'type': regulations.type.name,
                    'description': regulations.description,
                    'date': regulations.created,
                    'status': regulations.status.name,
                })
        return framework_data

    def __get_regulation_formatted_data(self, regulation, regulation_rating_obj, substance_module_permission):
        regulation_data = {
            'type': 'regulation',
            'id': regulation.id,
            'date': None,
            'status': regulation.status.name,
            'issuing_body': {
                'id': regulation.regulatory_framework.issuing_body.id,
                'name': regulation.regulatory_framework.issuing_body.name
            },
            'regulatory-framework': {
                'id': regulation.regulatory_framework.id,
                'name': regulation.regulatory_framework.name,
                'date': regulation.regulatory_framework.created,
                'text': regulation.regulatory_framework.description,
                'status': regulation.regulatory_framework.status.name,
            } if regulation.regulatory_framework.review_status == 'o' else {},
            'name': regulation.name,
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(self.organization_id,
                                                                                              regulation.product_categories,
                                                                                              serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(self.organization_id,
                                                                                                regulation.material_categories,
                                                                                                serialize=True),
            'milestones': [],
            'regions': RegionIdNameSerializer(regulation.regulatory_framework.regions, many=True).data,
            'impact_rating': regulation_rating_obj,
            'substances': RelevantSubstanceService().get_organization_relevant_substance_data(
                self.organization_id, data_name='regulation', data_id=regulation.id, serializer=True)
            if substance_module_permission else []
        }
        return regulation_data


class DashboardTimelineApiView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self):
        super().__init__()
        self.from_date = None
        self.to_date = None

    def post(self, request):
        try:
            filters = {
                'topics': request.data.get('topics', None),
                'regions': request.data.get('region', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'from_date': request.data.get('from', None),
                'to_date': request.data.get('to', None),
                'news': request.data.get('news', None),
                'regulations': request.data.get('regulations', None),
                'frameworks': request.data.get('frameworks', None),
                'related_products': request.data.get('related_products', None),
                'related_regulations': request.data.get('related_regulations', None),
                'related_frameworks': request.data.get('related_frameworks', None)
            }
            self.from_date = datetime.strptime(filters['from_date'], "%Y-%m-%d").replace(tzinfo=utc) if filters[
                'from_date'] else None
            self.to_date = datetime.strptime(filters['to_date'], "%Y-%m-%d").replace(tzinfo=utc, hour=23) if filters[
                'to_date'] else None
            response_date = {}
            organization_id = request.user.organization_id

            dashboard_service = DashboardService()

            if dashboard_service.is_return_data(filters, 'news'):
                news_search = dashboard_service.get_filtered_news_queryset(filters, organization_id)
                news_search = news_search[0:news_search.count()]
                response_date = self.get_news_data(news_search, response_date)

            if dashboard_service.is_return_data(filters, 'regulations'):
                regulation_search = dashboard_service.get_filtered_regulation_queryset(filters, organization_id)
                regulation_search = regulation_search[0:regulation_search.count()]
                response_date = self.get_regulation_data(regulation_search, response_date, organization_id)

            if dashboard_service.is_return_data(filters, 'frameworks'):
                framework_search = dashboard_service.get_filtered_regulatory_framework_queryset(filters, organization_id)
                framework_search = framework_search[0:framework_search.count()]
                response_date = self.get_framework_data(framework_search, response_date, organization_id)

            return Response(response_date, status=status.HTTP_200_OK)
        except Exception as ex:
            is_es_rebuild = DashboardService().check_es_exception(ex)
            return self.post(request) if is_es_rebuild \
                else Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_formatted_dict(new_data, date):
        if not isinstance(new_data.get(str(date.year)), dict):
            new_data[str(date.year)] = {}
        if not isinstance(new_data.get(str(date.year)).get(str(date.month)), dict):
            new_data[str(date.year)][str(date.month)] = {}
        if not isinstance(new_data[str(date.year)][str(date.month)].get(str(date.day)), dict):
            new_data[str(date.year)][str(date.month)][str(date.day)] = {'news': [], 'regulations': [], 'frameworks': []}

        return new_data

    def get_news_data(self, news_search, new_data):
        for news in news_search:
            date = news.pub_date
            new_data = self.get_formatted_dict(new_data, date)
            new_data[str(date.year)][str(date.month)][str(date.day)]['news'].append(news.id)
        return new_data

    def get_regulation_data(self, regulation_search, new_data, organization_id):
        related_milestones_ids = RelevantRegulationService().get_relevant_milestone_id_organization(organization_id)
        for regulation in regulation_search:
            for milestone in regulation.regulation_milestone:
                if IdSearchService().does_id_exit_in_sorted_list(related_milestones_ids, milestone.id):
                    if milestone.from_date and self.from_date <= milestone.from_date <= self.to_date:
                        date = milestone.from_date
                        new_data = self.get_formatted_dict(new_data, date)
                        new_data[str(date.year)][str(date.month)][str(date.day)]['regulations'].append(regulation.id)
        return new_data

    def get_framework_data(self, framework_search, new_data, organization_id):
        related_milestones_ids = RelevantRegulationService().get_relevant_milestone_id_organization(organization_id)
        for framework in framework_search:
            for milestone in framework.regulatory_framework_milestone:
                if IdSearchService().does_id_exit_in_sorted_list(related_milestones_ids, milestone.id):
                    if milestone.from_date and self.from_date <= milestone.from_date <= self.to_date:
                        date = milestone.from_date
                        new_data = self.get_formatted_dict(new_data, date)
                        new_data[str(date.year)][str(date.month)][str(date.day)]['frameworks'].append(framework.id)
        return new_data


class DashboardFilterOptionsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            topics = request.data.get('topics', None)
            regions = request.data.get('regions', None)
            product_categories = request.data.get('product_categories', None)
            material_categories = request.data.get('material_categories', None)
            related_products = request.data.get('related_products', None)
            related_regulations = request.data.get('related_regulations', None)
            related_frameworks = request.data.get('related_frameworks', None)
            from_date = request.data.get('from_date', None)
            to_date = request.data.get('to_date', None)
            news = request.data.get('news', None)
            regulations = request.data.get('regulations', None)
            frameworks = request.data.get('frameworks', None)

            filters = {
                'topics': topics,
                'regions': regions,
                'product_categories': product_categories,
                'material_categories': material_categories,
                'from_date': from_date,
                'to_date': to_date,
                'news': news,
                'regulations': regulations,
                'frameworks': frameworks,
                'related_products': related_products,
                'related_regulations': related_regulations,
                'related_frameworks': related_frameworks,
            }

            response_data = {'regions': [], 'product_categories': [], 'material_categories': [], 'topics': []}
            organization_id = request.user.organization_id
            relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(organization_id)

            if topics or regions or product_categories or material_categories or related_products or related_regulations \
                    or related_frameworks or (from_date and to_date) or news or regulations or frameworks:

                dashboard_service = DashboardService()

                queryset_news = []
                framework_queryset = []
                regulation_queryset = []

                organization_service = OrganizationService()
                organization_product_category_ids = organization_service.get_organization_product_category_ids(
                    organization_id)
                organization_material_category_ids = organization_service.get_organization_material_category_ids(
                    organization_id)

                if dashboard_service.is_return_data(filters, 'news'):
                    queryset_news = dashboard_service.get_filtered_news_queryset(filters, organization_id)
                    queryset_news = queryset_news[0:queryset_news.count()]

                if dashboard_service.is_return_data(filters, 'frameworks'):
                    framework_queryset = dashboard_service.get_filtered_regulatory_framework_queryset(filters, organization_id)
                    framework_queryset = framework_queryset[0:framework_queryset.count()]

                if dashboard_service.is_return_data(filters, 'regulations'):
                    regulation_queryset = dashboard_service.get_filtered_regulation_queryset(filters, organization_id)
                    regulation_queryset = regulation_queryset[0:regulation_queryset.count()]

                for news in queryset_news:

                    for region in news.regions:
                        obj = {'id': region.id, 'name': region.name}
                        if self.is_unique(obj, response_data['regions']):
                            response_data['regions'].append(obj)

                    for product_category in news.product_categories:
                        obj = {'id': product_category.id, 'name': product_category.name}
                        if product_category.id in organization_product_category_ids and self.is_unique(obj, response_data['product_categories']):
                            response_data['product_categories'].append(obj)

                    for material_cat in news.material_categories:
                        obj = {
                            'id': material_cat.id,
                            'name': material_cat.name,
                            'industry': {
                                'id': material_cat.industry.id,
                                'name': material_cat.industry.name
                            }
                        }
                        if material_cat.id in organization_material_category_ids and self.is_unique(obj, response_data['material_categories']):
                            response_data['material_categories'].append(obj)

                    for news_category in news.news_categories:
                        topic = news_category.topic
                        if topic and topic.id in relevant_topics_ids:
                            obj = {'id': topic.id, 'name': topic.name}
                            if self.is_unique(obj, response_data['topics']):
                                response_data['topics'].append(obj)

                for framework in framework_queryset:
                    for product_category in framework.product_categories:
                        obj = {'id': product_category.id, 'name': product_category.name}
                        if product_category.id in organization_product_category_ids and self.is_unique(obj, response_data['product_categories']):
                            response_data['product_categories'].append(obj)

                    for material_cat in framework.material_categories:
                        obj = {
                            'id': material_cat.id,
                            'name': material_cat.name,
                            'industry': {
                                'id': material_cat.industry.id,
                                'name': material_cat.industry.name
                            }
                        }
                        if material_cat.id in organization_material_category_ids and self.is_unique(obj, response_data['material_categories']):
                            response_data['material_categories'].append(obj)

                    for topic in framework.topics:
                        if topic.id in relevant_topics_ids:
                            obj = {'id': topic.id, 'name': topic.name}
                            if self.is_unique(obj, response_data['topics']):
                                response_data['topics'].append(obj)
                    for region in framework.regions:
                        obj = {'id': region.id, 'name': region.name}
                        if self.is_unique(obj, response_data['regions']):
                            response_data['regions'].append(obj)

                for regulation in regulation_queryset:
                    for topic in regulation.topics:
                        if topic.id in relevant_topics_ids:
                            obj = {'id': topic.id, 'name': topic.name}
                            if self.is_unique(obj, response_data['topics']):
                                response_data['topics'].append(obj)

                    for product_category in regulation.product_categories:
                        obj = {'id': product_category.id, 'name': product_category.name}
                        if product_category.id in organization_product_category_ids and self.is_unique(obj, response_data['product_categories']):
                            response_data['product_categories'].append(obj)

                    for material_cat in regulation.material_categories:
                        obj = {
                            'id': material_cat.id,
                            'name': material_cat.name,
                            'industry': {
                                'id': material_cat.industry.id,
                                'name': material_cat.industry.name
                            }
                        }
                        if material_cat.id in organization_material_category_ids and self.is_unique(obj, response_data['material_categories']):
                            response_data['material_categories'].append(obj)

            else:

                response_data = self.get_all_options(response_data, relevant_topics_ids)

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as ex:
            is_es_rebuild = DashboardService().check_es_exception(ex)
            return self.post(request) if is_es_rebuild \
                else Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_all_options(news_data, relevant_topics_ids):
        queryset_topic = TopicDocument.search()
        queryset_region = RegionDocument.search()
        queryset_product_category = ProductCategoryDocument.search()
        queryset_material_category = MaterialCategoryDocument.search()

        for topic in queryset_topic:
            if topic.id in relevant_topics_ids:
                news_data['topics'].append({'id': topic.id, 'name': topic.name})

        for region in queryset_region:
            news_data['regions'].append({'id': region.id, 'name': region.name})

        for product_category in queryset_product_category:
            news_data['product_categories'].append({'id': product_category.id, 'name': product_category.name})

        for material_category in queryset_material_category:
            obj = {
                'id': material_category.id,
                'name': material_category.name,
                'industry': {
                    'id': material_category.industry.id,
                    'name': material_category.industry.name
                }
            }
            news_data['material_categories'].append(obj)

        return news_data

    @staticmethod
    def is_unique(obj, response):
        return obj not in response
