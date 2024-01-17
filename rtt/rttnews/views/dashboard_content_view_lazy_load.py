from datetime import datetime

import pytz
from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.permissions import has_substance_module_permission
from rttcore.services.dashboard_services import DashboardService
from rttcore.services.system_filter_service import SystemFilterService

from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.serializers.serializers import RegionIdNameSerializer, TopicIdNameSerializer
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService

utc = pytz.UTC


class DashboardContentLazyLoadApiView(APIView):
    permission_classes = [IsAuthenticated]
    rating_search_service = RatingSearchService()
    organization_id = None

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
            limit = request.data.get('limit', 10)
            news_skip = request.data.get('news_skip', 0)
            milestone_skip = request.data.get('milestone_skip', 0)

            from_date = datetime.strptime(filters['from_date'], "%Y-%m-%d").replace(tzinfo=utc) if filters[
                'from_date'] else None
            to_date = datetime.strptime(filters['to_date'], "%Y-%m-%d").replace(tzinfo=utc, hour=23) if filters[
                'to_date'] else None
            self.organization_id = request.user.organization_id
            substance_module_permission = has_substance_module_permission(self.organization_id)
            result = []
            dashboard_service = DashboardService()

            """get news_queryset and milestone_queryset"""
            queryset_news = dashboard_service.get_filtered_news_queryset(filters,
                                                                         self.organization_id).sort('-pub_date')
            queryset_milestone = self.get_filtered_milestone_doc_queryset(filters, self.organization_id,
                                                                          from_date, to_date)

            """pagination calculation"""
            news_count, milestone_count = self.get_news_milestone_count(filters, queryset_news, queryset_milestone)
            news_limit, milestone_limit = self.get_news_milestone_limit(limit, news_count, news_skip,
                                                                        milestone_count, milestone_skip)
            """
            news data
            """
            if dashboard_service.is_return_data(filters, 'news'):
                queryset_news = queryset_news[news_skip: news_skip + news_limit]
                rel_regulation_ids_org = RelevantRegulationService().get_relevant_regulation_id_organization(
                    self.organization_id)
                rel_framework_ids_org = RelevantRegulationService().get_relevant_regulatory_framework_id_organization(
                    self.organization_id)
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
                                                      rel_regulation.id in rel_regulation_ids_org, news.regulations))
                    for regulation in relevant_regulation:
                        regulation_rating_obj = self.rating_search_service.\
                            get_regulation_rating_obj(self.organization_id, regulation.id)
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
                                                                rel_reg_fw.id in rel_framework_ids_org,
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

                    result.append(news_data)

            """
            milestone data
            """
            if DashboardService().is_return_data(filters, 'frameworks') or DashboardService().is_return_data(
                    filters, 'regulations'):
                queryset_milestone = queryset_milestone[milestone_skip: milestone_skip + milestone_limit]
                for milestone in queryset_milestone:
                    # For regulatory_framework
                    if milestone.regulatory_framework:
                        rf_rating_obj = self.rating_search_service.get_framework_rating_obj(
                            self.organization_id, milestone.regulatory_framework.id)

                        framework_data = self.__get_regulatory_framework_formatted_data(
                            milestone.regulatory_framework, rf_rating_obj, substance_module_permission)

                        framework_data['date'] = milestone.from_date
                        framework_data['milestones'] = [{
                            'id': milestone.id,
                            'name': milestone.name,
                            'type': milestone.type.name,
                            'description': milestone.description,
                            'date': milestone.from_date,
                        }]
                        result.append(framework_data.copy())
                    # For regulation
                    elif milestone.regulation:
                        regulation_rating_obj = self.rating_search_service.\
                            get_regulation_rating_obj(self.organization_id, milestone.regulation.id)
                        regulation_data = self.__get_regulation_formatted_data(
                            milestone.regulation, regulation_rating_obj, substance_module_permission)
                        regulation_data['date'] = milestone.from_date
                        regulation_data['milestones'] = [{
                            'id': milestone.id,
                            'name': milestone.name,
                            'type': milestone.type.name,
                            'description': milestone.description,
                            'date': milestone.from_date
                        }]
                        result.append(regulation_data.copy())
            result.sort(key=lambda data: data['date'], reverse=True)
            response = {
                "news_count": news_count,
                "next_news_skip": news_skip + news_limit,
                "milestone_count": milestone_count,
                "next_milestone_skip": milestone_skip + milestone_limit,
                "results": result
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            is_es_rebuild = DashboardService().check_es_exception(ex)
            return self.post(request) if is_es_rebuild \
                else Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def __get_regulatory_framework_formatted_data(self, regulatory, rf_rating_obj, substance_module_permission):
        framework_data = {
            'type': 'regulatory-framework',
            'id': regulatory.id,
            'date': None,
            'status': regulatory.status.name,
            'issuing_body': {'id': regulatory.issuing_body.id, 'name': regulatory.issuing_body.name},
            'name': regulatory.name,
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                self.organization_id, regulatory.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                self.organization_id, regulatory.material_categories, serialize=True),
            'regulations': [],
            'milestones': [],
            'regions': RegionIdNameSerializer(regulatory.regions, many=True).data,
            'impact_rating': rf_rating_obj,
            'topics': TopicIdNameSerializer(regulatory.topics, many=True).data,
            'substances': RelevantSubstanceService().get_organization_relevant_substance_data(
                self.organization_id, data_name='framework', data_id=regulatory.id, serializer=True)
            if substance_module_permission else []
        }
        regulations_doc_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(
            self.organization_id)
        regulations_doc_qs = regulations_doc_qs.filter(
            Q('match', regulatory_framework__id=regulatory.id)
        )
        regulations_doc_qs = regulations_doc_qs[0:regulations_doc_qs.count()]
        for regulations in regulations_doc_qs:
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
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                self.organization_id, regulation.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                self.organization_id, regulation.material_categories, serialize=True),
            'milestones': [],
            'regions': RegionIdNameSerializer(regulation.regulatory_framework.regions, many=True).data,
            'impact_rating': regulation_rating_obj,
            'substances': RelevantSubstanceService().get_organization_relevant_substance_data(
                self.organization_id, data_name='regulation', data_id=regulation.id, serializer=True)
            if substance_module_permission else []
        }
        return regulation_data

    @staticmethod
    def get_news_milestone_limit(limit, news_count, news_skip, milestone_count, milestone_skip):
        limit_half = limit // 2
        if news_count < milestone_count:
            news_limit = min(limit_half, news_count - news_skip)
            if news_limit < 0:
                news_limit = 0
            milestone_limit = min(limit - news_limit, milestone_count - milestone_skip)
            if milestone_limit < 0:
                milestone_limit = 0
        else:
            milestone_limit = min(limit_half, milestone_count - milestone_skip)
            if milestone_limit < 0:
                milestone_limit = 0
            news_limit = min(limit - milestone_limit, news_count - news_skip)
            if news_limit < 0:
                news_limit = 0
        return news_limit, milestone_limit

    @staticmethod
    def get_news_milestone_count(filters, news_doc_qs, milestone_doc_qs):
        if DashboardService().is_return_data(filters, 'news'):
            news_count = news_doc_qs.count()
        else:
            news_count = 0
        if DashboardService().is_return_data(filters, 'frameworks') or DashboardService().is_return_data(
                filters, 'regulations'):
            milestone_count = milestone_doc_qs.count()
        else:
            milestone_count = 0
        return news_count, milestone_count

    @staticmethod
    def get_filtered_milestone_doc_queryset(filters, organization_id, from_date, to_date):
        # generate framework ids for milestone
        framework_ids = []
        if DashboardService().is_return_data(filters, 'frameworks'):
            queryset_regulatory = DashboardService().get_filtered_regulatory_framework_queryset(
                filters, organization_id).source(['id'])
            queryset_regulatory = queryset_regulatory[0:queryset_regulatory.count()]
            for framework in queryset_regulatory:
                framework_ids.append(framework.id)

        # generate regulation ids for milestone
        regulation_ids = []
        if DashboardService().is_return_data(filters, 'regulations'):
            queryset_regulation = DashboardService().get_filtered_regulation_queryset(
                filters, organization_id).source(['id'])
            queryset_regulation = queryset_regulation[0:queryset_regulation.count()]
            for regulation in queryset_regulation:
                regulation_ids.append(regulation.id)

        # apply system filter for milestone using framework and regulation id get from dashboard service
        queryset_milestone = SystemFilterService().get_system_filtered_milestone_document_queryset(
            organization_id).filter(
            Q('terms', regulation__id=regulation_ids) |
            Q('terms', regulatory_framework__id=framework_ids)
        ).sort('-from_date')

        if from_date and to_date:
            queryset_milestone = queryset_milestone.filter(
                Q('range', from_date={'gte': from_date, 'lte': to_date})
            )
        return queryset_milestone
