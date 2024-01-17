from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from elasticsearch_dsl import Q

from rttcore.permissions import IsActiveSubstanceModule
from rttcore.services.dashboard_services import DashboardService
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.serializers.serializers import RegionIdNameSerializer
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService


class SubstanceNews(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of news topic type ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'source_types': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of news source type ID',
                                           items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING, description='search key_word in news_title'),
            'sort_order': openapi.Schema(type=openapi.TYPE_STRING, description='Sorting: asc/desc, default is desc.'),
            'limit': openapi.Schema(type=openapi.TYPE_INTEGER, description='For pagination.Default is 10.'),
            'skip': openapi.Schema(type=openapi.TYPE_INTEGER),
        }
    ))
    def post(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-582
        """
        try:
            filters = {
                'regions': request.data.get('regions', None),
                'topics': request.data.get('topics', None),
                'source_types': request.data.get('source_types', None),
                'search': request.data.get('search', None)
            }
            sort_order = request.data.get('sort_order', 'desc')
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            substance_id = int(substance_id)
            organization_id = request.user.organization_id
            news_list = []
            queryset_news = DashboardService().get_filtered_news_queryset(filters, organization_id).filter(
                Q('nested',
                  path='substances',
                  query=Q('match', substances__id=substance_id))
            )
            if filters.get('source_types', None):
                queryset_news = queryset_news.filter(
                    Q('terms', source__type__id=filters['source_types'])
                )
            queryset_news = queryset_news.sort({
                "news_relevance.relevancy": {
                    "order": sort_order,
                    "nested_path": "news_relevance",
                    "nested_filter": {
                        "term": {
                            "news_relevance.organization.id": organization_id
                        }
                    }
                }
            }, {"pub_date": {"order": "desc"}})

            count = queryset_news.count()
            queryset_news = queryset_news[skip:skip + limit]
            relevant_regulation_ids_org = RelevantRegulationService().get_relevant_regulation_id_organization(
                organization_id)
            relevant_regulatory_framework_ids_org = RelevantRegulationService(). \
                get_relevant_regulatory_framework_id_organization(organization_id)
            for news in queryset_news:
                news_list.append(self.get_news_data_obj(news, organization_id, relevant_regulation_ids_org,
                                                        relevant_regulatory_framework_ids_org))
            response = {
                'count': count,
                'results': news_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_news_data_obj(news, organization_id, relevant_regulation_ids_org, relevant_regulatory_framework_ids_org):
        news_rating_obj = RatingSearchService().get_news_rating_obj(organization_id, news.id, news.news_relevance)
        region_list = RegionIdNameSerializer(news.regions, many=True).data
        news_data = {
            'id': news.id,
            'name': news.title,
            'body': news.body,
            'pub_date': news.pub_date,
            'status': 'New' if news.status == 'n' else 'Selected' if news.status == 's' else 'Discharged',
            'impact_rating': news_rating_obj,
            'source': {'id': news.source.id, 'name': news.source.name},
            'regions': region_list,
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                organization_id, news.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                organization_id, news.material_categories, serialize=True),
            'regulations': [],
            'frameworks': []
        }
        relevant_regulation = list(filter(lambda rel_regulation:
                                          rel_regulation.id in relevant_regulation_ids_org,
                                          news.regulations))
        for regulation in relevant_regulation:
            news_data['regulations'].append({
                'id': regulation.id,
                'name': regulation.name,
                'status': regulation.status.name,
                'description': regulation.description
            })
        relevant_regulatory_framework = list(filter(lambda rel_reg_fw:
                                                    rel_reg_fw.id in relevant_regulatory_framework_ids_org,
                                                    news.regulatory_frameworks))
        for framework in relevant_regulatory_framework:
            news_data['frameworks'].append({
                'id': framework.id,
                'name': framework.name,
                'status': framework.status.name,
                'description': framework.description
            })
        return news_data
