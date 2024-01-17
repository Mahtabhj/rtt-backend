import logging
from django.db.models import Q as DQ
from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.services.dashboard_services import DashboardService
from rttcore.services.system_filter_service import SystemFilterService
from rttnews.documents import RegionDocument
from rttregulation.documents import TopicDocument
from rttorganization.services.organization_services import OrganizationService
from rttproduct.serializers.serializers import ProductCategoryIdNameSerializer, \
    MaterialCategoryIdNameShortNameSerializer
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.documents import RegulationDocument, RegulatoryFrameworkDocument, \
    MilestoneDocument
from rttregulation.models.models import RegulationMilestone, RegulatoryFrameworkRating, RegulationRatingLog
from rttregulation.serializers.serializers import TopicIdNameSerializer, RegionIdNameSerializer
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.regulatory_framework_content_service import RegulatoryFrameworkContentService
from rttregulation.services.relevant_topic_service import RelevantTopicService
from rttcore.permissions import has_substance_module_permission
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService

logger = logging.getLogger(__name__)


class DashboardMilestoneSearchApi(APIView):
    permission_classes = (IsAuthenticated,)
    new_data = {}

    def get(self, request):
        try:
            self.organization_id = request.user.organization_id
            self.new_data = {}
            from_date = self.request.GET.get('from_date', None)
            to_date = self.request.GET.get('to_date', None)
            self.get_milestone_data(from_date, to_date)
            return Response(self.new_data, status=status.HTTP_200_OK)
        except Exception as ex:
            is_es_rebuild = DashboardService().check_es_exception(ex)
            return self.get(request) if is_es_rebuild \
                else Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_milestone_data(self, from_date, to_date):
        milestone_search = SystemFilterService().get_system_filtered_milestone_document_queryset(
            self.organization_id).sort('from_date')
        milestone_queryset = self.__apply_milestone_filter(milestone_search, from_date, to_date)
        milestones = milestone_queryset.execute().hits
        for milestone in milestones:
            from_date = milestone['from_date']
            year = str(from_date.year)
            month = str(from_date.month)
            day = str(from_date.day)

            if not isinstance(self.new_data.get(year), dict):
                self.new_data[year] = {}
            if not isinstance(self.new_data.get(year).get(month), dict):
                self.new_data[year][month] = {}
            if not isinstance(self.new_data.get(year).get(month).get(day), list):
                self.new_data[year][month][day] = []

            milestone_from = self.get_milestone_from(milestone)
            self.new_data[str(from_date.year)][str(from_date.month)][str(from_date.day)].append({
                'from': milestone_from['from'],
                'id': milestone_from['id'],
                'name': milestone.name,
                'milestone_type': milestone.type.name
            })

    @staticmethod
    def get_milestone_from(milestone):
        milestone_from = {'from': '', 'id': 0}
        if milestone.regulation:
            milestone_from['from'] = 'regulation'
            milestone_from['id'] = milestone.regulation.id
        elif milestone.regulatory_framework:
            milestone_from['from'] = 'regulatory-framework'
            milestone_from['id'] = milestone.regulatory_framework.id
        return milestone_from

    @staticmethod
    def __apply_milestone_filter(milestone_search, from_date, to_date):
        if from_date and to_date:
            milestone_search = milestone_search.filter(
                'range', from_date={'gte': from_date, 'lte': to_date}
            )
        elif from_date:
            milestone_search = milestone_search.filter(
                'range', from_date={'gte': from_date}
            )
        elif to_date:
            milestone_search = milestone_search.filter(
                'range', from_date={'lte': to_date}
            )
        return milestone_search[0:milestone_search.count()]

    def __provide_regulation_data(self, s_regulation):
        queryset_regulation = RegulationDocument().search()
        s_regulation.aggs.bucket(name='regulation_over_time', agg_type='date_histogram',
                                 **{"field": "created",
                                    "calendar_interval": "day",
                                    "keyed": True,
                                    'format': 'yyy-MM-dd',
                                    "min_doc_count": 1}).result(s_regulation, queryset_regulation)
        regulations = queryset_regulation.execute().hits
        result_regulation = s_regulation.execute().aggregations.regulation_over_time.buckets
        for data in regulations:
            date = data['created']
            regulation_milestone_len = len(data.regulation_milestone)
            if not isinstance(self.new_data.get(str(date.year)), dict):
                self.new_data[str(date.year)] = {}
            if not isinstance(self.new_data.get(str(date.year)).get(str(date.month)), dict):
                self.new_data[str(date.year)][str(date.month)] = {}
            if not isinstance(self.new_data[str(date.year)][str(date.month)].get(str(date.day)), dict):
                self.new_data[str(date.year)][str(date.month)][str(date.day)] = []

            for item in data.regulation_milestone:
                self.new_data[str(date.year)][str(date.month)][str(date.day)].append({
                    'from': 'regulation',
                    'id': data['id'],
                    'name': item.name,
                    'milestone_type': item.type.name,
                })

    def __provide_framework_data(self, s_regulation):
        queryset_framework = RegulatoryFrameworkDocument().search()
        s_regulation.aggs.bucket(name='framework_over_time', agg_type='date_histogram',
                                 **{"field": "created",
                                    "calendar_interval": "day",
                                    "keyed": True,
                                    'format': 'yyy-MM-dd',
                                    "min_doc_count": 1}).result(s_regulation, queryset_framework)
        framework = queryset_framework.execute().hits
        result_regulation = s_regulation.execute().aggregations.framework_over_time.buckets
        for data in framework:
            date = data['created']
            framework_milestone_len = len(data.regulatory_framework_milestone)
            if not isinstance(self.new_data.get(str(date.year)), dict):
                self.new_data[str(date.year)] = {}
            if not isinstance(self.new_data.get(str(date.year)).get(str(date.month)), dict):
                self.new_data[str(date.year)][str(date.month)] = {}
            if not isinstance(self.new_data[str(date.year)][str(date.month)].get(str(date.day)), dict):
                self.new_data[str(date.year)][str(date.month)][str(date.day)] = []
            # if framework_milestone_len > 0 and not isinstance(
            #         self.new_data[str(date.year)][str(date.month)][str(date.day)].get('milestones'), dict):
            #     self.new_data[str(date.year)][str(date.month)][str(date.day)]['milestones'] = []

            for item in data.regulatory_framework_milestone:
                self.new_data[str(date.year)][str(date.month)][str(date.day)].append(
                    {'from': 'regulatory-framework', 'id': data['id'], 'name': item.name, 'milestone_type':
                        item.type.name})

            # if framework_milestone_len > 0 and len(
            #         self.new_data[str(date.year)][str(date.month)][str(date.day)]['milestones']) > 0:
            #     self.new_data[str(date.year)][str(date.month)][str(date.day)]['regulatory-frameworks'] = \
            #         result_regulation[str(date).split(' ')[0]].doc_count


class RegulatoryFrameworkContentApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        topics = request.data.get('topics', None)
        regions = request.data.get('regions', None)
        products = request.data.get('product_categories', None)
        materials = request.data.get('material_categories', None)
        group_by = request.data.get('group_by', None)  # regions, topics, impact
        limit = request.data.get('limit', 10)
        skip = request.data.get('skip', 0)
        is_muted = request.data.get('is_muted', False)
        frameworks = request.data.get('regulatory_frameworks', None)
        self.organization_id = request.user.organization_id
        substance_module_permission = has_substance_module_permission(self.organization_id)

        framework_list = []
        group_by_response = []

        framework_queryset = RegulatoryFrameworkContentService(
            self.organization_id).get_filtered_regulatory_framework_queryset(topics, products, materials, regions,
                                                                             is_muted, frameworks,
                                                                             apply_regulation_mute=True)
        if group_by:
            if group_by in ['regions', 'topics']:
                agg_dict = self.get_region_or_topics_group_by_dict(group_by, group_by_field_id=group_by + '.id')
            else:
                agg_dict = self.get_rating_group_by_dict(self.organization_id)
            regulatory_framework_doc_qs = framework_queryset.update_from_dict(agg_dict).execute()
            group_by_doc_queryset = None
            for framework_doc in regulatory_framework_doc_qs.aggregations:
                group_by_doc_queryset = framework_doc
            if group_by in ['regions', 'topics']:
                for group_by_doc_qs in group_by_doc_queryset.results.buckets:
                    group_by_response.append(
                        self.get_object_obj(group_by_doc_qs.key, group_by_doc_qs.doc_count, group_by))
            else:
                for group_by_doc_qs in group_by_doc_queryset.filter_regulatory_framework_rating.results.buckets:
                    group_by_response.append({
                        'id': group_by_doc_qs.key,
                        'name': group_by_doc_qs.key,
                        'count': group_by_doc_qs.doc_count
                    })
            if group_by == 'impact':
                framework_queryset = framework_queryset.filter(
                    ~Q('nested',
                       path='regulatory_framework_rating',
                       query=Q('match', regulatory_framework_rating__organization__id=self.organization_id))
                )
                if framework_queryset:
                    found, idx = self.is_name_exists_in_list(group_by_response, 0)
                    if found:
                        group_by_response[idx]['count'] += framework_queryset.count()
                    else:
                        group_by_response.append({
                            'id': 0,
                            'name': 0,
                            'count': framework_queryset.count()
                        })
        else:
            framework_queryset = framework_queryset[skip:skip + limit]
            system_filtered_regulation_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(
                self.organization_id, is_muted=is_muted).source(['id']).sort('id')
            system_filtered_regulation_qs = system_filtered_regulation_qs[0:system_filtered_regulation_qs.count()]
            rel_reg_ids = []
            for regulation in system_filtered_regulation_qs:
                rel_reg_ids.append(regulation.id)
            for framework in framework_queryset:
                framework_obj = RegulatoryFrameworkContentService(
                    self.organization_id).get_serialized_framework_object(framework, substance_module_permission,
                                                                          rel_reg_ids, is_muted)
                framework_list.append(framework_obj)

        if group_by:
            group_by_response.sort(key=lambda x: x['name'], reverse=(True if group_by == 'impact' else False))
            response = group_by_response
        else:
            response = {
                'count': framework_queryset.count(),
                'results': framework_list
            }

        return Response(response, status=status.HTTP_200_OK)

    @staticmethod
    def is_name_exists_in_list(list_data, name):
        """
        Return found and index.
        """
        for index, item in enumerate(list_data):
            if item['name'] == name:
                return True, index
        return False, -1

    def __apply_group_by(self, framework_obj, group_by, response):
        if group_by == 'regions':
            for region in framework_obj['regions']:
                self.__save_group_by_data(region['name'], framework_obj, response)

        elif group_by == 'topics':
            for topic in framework_obj['topics']:
                self.__save_group_by_data(topic['name'], framework_obj, response)

        elif group_by == 'impact':
            rating = framework_obj['impact_rating']['rating'] if framework_obj['impact_rating'] else 0
            self.__save_group_by_data(rating, framework_obj, response)

    def __save_group_by_data(self, group_by_name, framework_obj, response):
        found, index = self.is_name_exists_in_list(response, group_by_name)
        if found:
            response[index]['frameworks'].append(framework_obj)
        else:
            response.append({'name': group_by_name, 'frameworks': [framework_obj]})

    @staticmethod
    def get_region_or_topics_group_by_dict(group_by_field, group_by_field_id):
        region_group_by_dict = {
            "aggs": {
                group_by_field: {
                    "nested": {
                        "path": group_by_field
                    },
                    "aggs": {
                        "results": {
                            "terms": {
                                "field": group_by_field_id,
                                "size": 9999
                            }
                        }
                    }
                }
            }
        }
        return region_group_by_dict

    @staticmethod
    def get_object_obj(object_id, doc_count, group_by_field):
        result = None
        if group_by_field == 'regions':
            doc_queryset: RegionDocument = RegionDocument.search().filter('match', id=object_id)
        else:
            doc_queryset: TopicDocument = TopicDocument.search().filter('match', id=object_id)
        for doc_object in doc_queryset:
            result = {
                'id': doc_object.id,
                'name': doc_object.name,
                'count': doc_count
            }
        return result

    @staticmethod
    def get_rating_group_by_dict(organization_id):
        rating_group_by_dict = {
          "aggs": {
            "regulatory_framework_rating": {
              "nested": {
                "path": "regulatory_framework_rating"
              },
              "aggs": {
                "filter_regulatory_framework_rating": {
                  "filter": {
                    "bool": {
                      "filter": [
                        {
                          "term": {
                            "regulatory_framework_rating.organization.id": organization_id
                          }
                        }
                      ]
                    }
                  },
                  "aggs": {
                    "results": {
                      "terms": {
                        "field": "regulatory_framework_rating.rating",
                        "size": 9999
                      }
                    }
                  }
                }
              }
            }
          }
        }
        return rating_group_by_dict


class RegulatoryFrameworkFilterOptionsApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        __regions = request.data.get('regions', None)
        __topics = request.data.get('topics', None)
        __status = request.data.get('status', None)
        __product_categories = request.data.get('product_categories', None)
        __material_categories = request.data.get('material_categories', None)
        __regulatory_frameworks = request.data.get('regulatory_frameworks', None)
        self.organization_id = request.user.organization_id
        is_muted = request.data.get('is_muted', False)

        framework_data = {'topics': [], 'status': [], 'regions': [], 'product_categories': [],
                          'material_categories': []}

        queryset_framework = self.apply_framework_filter(__regions, __topics, __status, __product_categories,
                                                         __material_categories, is_muted, __regulatory_frameworks)

        organization_service = OrganizationService()
        organization_product_category_ids = organization_service.get_organization_product_category_ids(
            self.organization_id)
        organization_material_category_ids = organization_service.get_organization_material_category_ids(
            self.organization_id)
        relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(self.organization_id)
        for framework in queryset_framework:
            obj = {'id': framework.status.id, 'name': framework.status.name}
            if self.is_unique(obj, framework_data['status']):
                framework_data['status'].append(obj)

            for topics in framework.topics:
                if topics.id in relevant_topics_ids:
                    obj = {'id': topics.id, 'name': topics.name}
                    if self.is_unique(obj, framework_data['topics']):
                        framework_data['topics'].append(obj)

            for region in framework.regions:
                obj = {'id': region.id, 'name': region.name}
                if self.is_unique(obj, framework_data['regions']):
                    framework_data['regions'].append(obj)

            for product_category in framework.product_categories:
                obj = {'id': product_category.id, 'name': product_category.name}
                if product_category.id in organization_product_category_ids and \
                        self.is_unique(obj, framework_data['product_categories']):
                    framework_data['product_categories'].append(obj)

            for material_cat in framework.material_categories:
                obj = {
                    'id': material_cat.id,
                    'name': material_cat.name,
                    'industry': {
                        'id': material_cat.industry.id,
                        'name': material_cat.industry.name
                    }
                }
                if material_cat.id in organization_material_category_ids and \
                        self.is_unique(obj, framework_data['material_categories']):
                    framework_data['material_categories'].append(obj)

        return Response(framework_data, status=status.HTTP_200_OK)

    def apply_framework_filter(self, regions, topics, _status, product_categories, material_categories, is_muted,
                               regulatory_frameworks=None):
        queryset_framework = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
            self.organization_id, is_muted)

        if regulatory_frameworks:
            queryset_framework = queryset_framework.filter(Q('terms', id=regulatory_frameworks))
        if regions:
            queryset_framework = queryset_framework.filter(
                'nested',
                path='regions',
                query=Q('terms', regions__id=regions)
            )
        if topics:
            queryset_framework = queryset_framework.filter(
                'nested',
                path='topics',
                query=Q('terms', topics__id=topics)
            )
        if _status:
            queryset_framework = queryset_framework.filter(
                'terms',
                status__id=_status
            )
        if product_categories:
            queryset_framework = queryset_framework.filter(
                'nested',
                path='product_categories',
                query=Q('terms', product_categories__id=product_categories)
            )
        if material_categories:
            queryset_framework = queryset_framework.filter(
                'nested',
                path='material_categories',
                query=Q('terms', material_categories__id=material_categories)
            )
        return queryset_framework[0:queryset_framework.count()]

    @staticmethod
    def is_unique(obj, response):
        return obj not in response


class RegulationUpdates(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        organization = request.user.organization
        if organization is not None:
            milestone_search = SystemFilterService().get_system_filtered_milestone_document_queryset(
                organization.id).sort('-created')

            framework_impact_rating = RegulatoryFrameworkRating.objects.filter(organization=organization).order_by(
                '-created')[:10]
            regulation_impact_rating = RegulationRatingLog.objects.filter(organization=organization).order_by(
                '-created')[
                                       :10]
            result = []
            for data in milestone_search:
                if data.regulation:
                    obj = {
                        'id': data.regulation.id,
                        'type': 'milestone',
                        'is_regulation': True,
                        'date': data.created,
                        'title': data.regulation.name,
                        'name': data.name,
                        'text': data.description
                    }
                    result.append(obj)
                elif data.regulatory_framework:
                    obj = {
                        'id': data.regulatory_framework.id,
                        'type': 'milestone',
                        'is_regulation': False,
                        'date': data.created,
                        'title': data.regulatory_framework.name,
                        'name': data.name,
                        'text': data.description
                    }
                    result.append(obj)

            for data in regulation_impact_rating:
                obj = {
                    'id': data.regulation.id,
                    'type': 'rating',
                    'is_regulation': True,
                    'date': data.created,
                    'title': data.regulation.name,
                    'rating': data.rating,
                    'text': data.comment
                }
                result.append(obj)
            for data in framework_impact_rating:
                obj = {
                    'id': data.regulatory_framework.id,
                    'type': 'rating',
                    'is_regulation': False,
                    'date': data.created,
                    'title': data.regulatory_framework.name,
                    'rating': data.rating,
                    'text': data.comment
                }
                result.append(obj)
            result.sort(key=lambda r: r['date'], reverse=True)

            return Response(result[:10], status=status.HTTP_200_OK)
