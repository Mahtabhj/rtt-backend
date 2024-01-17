from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import copy
import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


from rttcore.permissions import IsActiveSubstanceModule
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttregulation.services.rating_search_service import RatingSearchService
from rttregulation.services.relevant_topic_service import RelevantTopicService
from rttsubstance.services.substance_details_filter_service import SubstanceDetailsFilterService
from rttcore.services.id_search_service import IdSearchService


class SubstanceDetailsRegulations(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of news topic type ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'status': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of status ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='search for framework and regulation'),
        }
    ))
    def post(self, request, substance_id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-581
        """
        try:
            filters = {
                'regions': request.data.get('regions', None),
                'topics': request.data.get('topics', None),
                'status': request.data.get('status', None),
            }
            search_keyword = request.data.get('search', None)
            sort_order = request.data.get('sort_order', 'desc')
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)
            substance_id = int(substance_id)
            organization_id = request.user.organization_id
            relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(organization_id)
            framework_list = []
            """ framework data """
            framework_doc_qs = SubstanceDetailsFilterService().get_filtered_framework_doc_queryset(
                organization_id, substance_id, filters, search_keyword)
            framework_doc_qs = self.get_sorted_framework_doc_queryset(framework_doc_qs, organization_id, sort_order)
            count = framework_doc_qs.count()
            framework_doc_qs = framework_doc_qs[skip:skip + limit]

            for framework in framework_doc_qs:
                framework_obj = self.get_framework_object(framework, organization_id, relevant_topics_ids)

                regulation_filters = copy.deepcopy(filters)
                regulation_filters['related_frameworks'] = [framework.id]

                """ regulation data """
                regulation_doc_qs = SubstanceDetailsFilterService().get_filtered_regulation_doc_queryset(
                    organization_id, substance_id, regulation_filters, search_keyword)
                regulation_doc_qs = self.get_sorted_regulation_doc_queryset(regulation_doc_qs, organization_id,
                                                                            sort_order)
                regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
                regulation_list = []
                for regulation in regulation_doc_qs:
                    regulation_obj = self.get_regulation_object(regulation, organization_id, relevant_topics_ids)
                    regulation_list.append(regulation_obj)
                framework_obj['regulations'] = regulation_list
                framework_list.append(framework_obj)

            response = {
                'count': count,
                'results': framework_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logging.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_sorted_framework_doc_queryset(framework_doc_qs, organization_id, sort_order):
        framework_doc_qs = framework_doc_qs.sort({
            "regulatory_framework_rating.rating": {
                "order": sort_order,
                "nested_path": "regulatory_framework_rating",
                "nested_filter": {
                    "term": {
                        "regulatory_framework_rating.organization.id": organization_id
                    }
                }
            }
        })
        return framework_doc_qs

    @staticmethod
    def get_sorted_regulation_doc_queryset(regulation_doc_qs, organization_id, sort_order):
        regulation_doc_qs = regulation_doc_qs.sort({
            "regulation_rating.rating": {
                "order": sort_order,
                "nested_path": "regulation_rating",
                "nested_filter": {
                    "term": {
                        "regulation_rating.organization.id": organization_id
                    }
                }
            }
        })
        return regulation_doc_qs

    @staticmethod
    def get_framework_object(framework, organization_id, relevant_topics_ids):
        topic_list = []
        region_list = []
        for topic in framework.topics:
            if IdSearchService().does_id_exit_in_sorted_list(relevant_topics_ids, topic.id):
                topic_list.append({'id': topic.id, 'name': topic.name})
        for region in framework.regions:
            region_list.append({'id': region.id, 'name': region.name})
        framework_obj = {
            'id': framework.id,
            'name': framework.name,
            'status': {'id': framework.status.id, 'name': framework.status.name},
            'topics': topic_list,
            'regions': region_list,
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                organization_id, framework.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                organization_id, framework.material_categories, serialize=True),
            'impact_rating': RatingSearchService().get_framework_rating_obj(organization_id, framework.id)
        }
        return framework_obj

    @staticmethod
    def get_regulation_object(regulation, organization_id, relevant_topics_ids):
        topic_list = []
        for topic in regulation.topics:
            if IdSearchService().does_id_exit_in_sorted_list(relevant_topics_ids, topic.id):
                topic_list.append({'id': topic.id, 'name': topic.name})
        regulation_obj = {
            'id': regulation.id,
            'name': regulation.name,
            'status': {'id': regulation.status.id, 'name': regulation.status.name},
            'topics': topic_list,
            'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                organization_id, regulation.product_categories, serialize=True),
            'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                organization_id, regulation.material_categories, serialize=True),
            'impact_rating': RatingSearchService().get_regulation_rating_obj(organization_id, regulation.id)
        }
        return regulation_obj
