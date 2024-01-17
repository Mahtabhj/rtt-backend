from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.services.system_filter_service import SystemFilterService
from rttdocument.documents import DocumentModelDocument
from rttnews.documents import NewsDocument
from rttproduct.documents import ProductDocument
from rttregulation.documents import RegulatoryFrameworkDocument, RegulationDocument, MilestoneDocument, TopicDocument
from rttregulation.models.core_models import Topic
from rttregulation.services.search_service import SearchService
from rttsubstance.services.substance_core_service import SubstanceCoreService
from rttcore.permissions import has_substance_module_permission


class SearchApiView(APIView):
    permission_classes = (IsAuthenticated,)
    search_service = SearchService()

    def get(self, request):
        keyword = request.GET.get('keyword', None)
        organization_id = request.user.organization_id
        response = []
        news_search = SystemFilterService().get_system_filtered_news_document_queryset(organization_id)
        product_search = ProductDocument.search().filter('match', organization__id=organization_id)
        milestone_search = SystemFilterService().get_system_filtered_milestone_document_queryset(organization_id)
        document_search = SystemFilterService().get_system_filtered_document_model_document_queryset(organization_id)
        regulation_search = SystemFilterService().get_system_filtered_regulation_document_queryset(organization_id)
        framework_search = SystemFilterService().get_system_filtered_regulatory_framework_queryset(organization_id)

        if keyword:
            keyword = keyword.lower()
            search_term = 'match' if keyword.__len__() >= 4 else 'prefix'
            news_search = news_search.query(Q(search_term, title=keyword) | Q('match_phrase', body=keyword)).sort("_score")
            product_search = product_search.query(Q(search_term, name=keyword) | Q('match_phrase', description=keyword)).sort(
                "_score")
            milestone_search = milestone_search.query(
                Q(search_term, name=keyword) | Q('match_phrase', description=keyword)).sort("_score")
            document_search = document_search.query(
                Q(search_term, title=keyword) | Q('match_phrase', description=keyword)).sort("_score")
            framework_search = framework_search.query(
                Q(search_term, name=keyword) | Q('match_phrase', description=keyword)).sort("_score")
            regulation_search = regulation_search.query(
                Q(search_term, name=keyword) | Q('match_phrase', description=keyword)).sort("_score")

        framework_response = self.__get_framework_data(framework_search, organization_id)
        response.append(framework_response)

        regulation_response = self.__get_regulation_data(regulation_search, organization_id)
        response.append(regulation_response)

        news_response = self.__get_news_data(news_search, organization_id)
        response.append(news_response)

        product_response = self.__get_product_data(product_search, organization_id)
        response.append(product_response)

        milestone_response = self.__get_milestone_data(milestone_search)
        response.append(milestone_response)

        document_response = self.__get_document_data(document_search)
        response.append(document_response)

        substance_response = self.__get_substance_data(organization_id, keyword)
        response.append(substance_response)

        return Response(response, status=status.HTTP_200_OK)

    def __get_framework_data(self, framework_search, organization_id):
        framework_response = {'title': 'Regulatory Frameworks', 'type': 'regulatoryFramework', 'items': []}
        for framework_doc in framework_search:
            framework_obj = self.search_service.get_framework_list_item(framework_doc, organization_id)
            framework_response['items'].append(framework_obj)
        return framework_response

    def __get_regulation_data(self, regulation_search, organization_id):
        regulation_response = {'title': 'Regulations', 'type': 'regulation', 'items': []}
        for regulation_doc in regulation_search:
            regulation_obj = self.search_service.get_regulation_list_item(regulation_doc, organization_id)
            regulation_response['items'].append(regulation_obj)
        return regulation_response

    def __get_news_data(self, news_search, organization_id):
        news_response = {'title': 'News', 'type': 'news', 'items': []}
        for news_doc in news_search:
            news_obj = self.search_service.get_news_list_item(news_doc, organization_id)
            news_response['items'].append(news_obj)
        return news_response

    def __get_product_data(self, product_search, organization_id):
        product_response = {'title': 'Products', 'type': 'product', 'items': []}
        for product_doc in product_search:
            product_obj = self.search_service.get_product_list_item(product_doc, organization_id)
            product_response['items'].append(product_obj)
        return product_response

    def __get_milestone_data(self, milestone_search):
        milestone_response = {'title': 'Milestones', 'type': 'milestone', 'items': []}
        for milestone_doc in milestone_search:
            milestone_obj = self.search_service.get_milestone_list_item(self.request.user.organization_id, milestone_doc)
            milestone_response['items'].append(milestone_obj)
        return milestone_response

    def __get_document_data(self, document_search):
        document_response = {'title': 'Documents', 'type': 'document', 'items': []}
        for document_doc in document_search:
            document_obj = self.search_service.get_document_list_item(document_doc)
            document_response['items'].append(document_obj)
        return document_response

    @staticmethod
    def __get_substance_data(organization_id, search_keyword):
        substance_response = {
            'title': 'Substances',
            'type': 'substance',
            'items': []
        }
        substance_module_permission = has_substance_module_permission(organization_id)
        if not substance_module_permission:
            return substance_response
        if search_keyword and search_keyword != '':
            substance_search = SubstanceCoreService().get_filtered_substance_queryset(organization_id,
                                                                                      search_keyword=search_keyword)
            for substance in substance_search:
                substance_obj = {
                    'id': substance.id,
                    'name': substance.name,
                    'ec_no': substance.ec_no,
                    'cas_no': substance.cas_no
                }
                substance_response['items'].append(substance_obj)
        return substance_response
