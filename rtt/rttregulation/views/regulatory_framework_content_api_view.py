import logging
import copy
from elasticsearch_dsl import Q
from rest_framework import status as response_status
from rest_framework.response import Response
from rest_framework.views import APIView

from rttnews.documents import RegionDocument
from rttregulation.documents import TopicDocument
from rttregulation.services.regulatory_framework_content_service import RegulatoryFrameworkContentService
from rttregulation.services.relevant_topic_service import RelevantTopicService

logger = logging.getLogger(__name__)


class RegulatoryFrameworkTabularContentApiView(APIView):

    def post(self, request):
        try:
            topics = request.data.get('topics', None)
            regions = request.data.get('regions', None)
            products = request.data.get('product_categories', None)
            materials = request.data.get('material_categories', None)
            group_by = request.data.get('group_by', None)  # regions, topics, impact
            is_muted = request.data.get('is_muted', False)
            frameworks = request.data.get('regulatory_frameworks', None)
            status = request.data.get('status', None)

            sort_order = request.data.get('sort_order', 'desc')  # default sort order is desc by rating
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)

            organization_id = request.user.organization_id
            framework_list = []
            relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(organization_id)

            # apply main filter
            framework_queryset = RegulatoryFrameworkContentService(
                organization_id).get_filtered_regulatory_framework_queryset(
                topics, products, materials, regions, is_muted, frameworks, apply_regulation_mute=True, status=status)

            # apply sort order
            framework_queryset = RegulatoryFrameworkContentService(
                organization_id).get_rating_sorted_regulatory_framework_doc_qs(framework_queryset, sort_order)
            # if group_by is applied
            if group_by:
                group_by_response = self.get_group_by_response(group_by, organization_id, framework_queryset)
                group_by_response.sort(key=lambda x: x['name'], reverse=(True if group_by == 'impact' else False))
                return Response(group_by_response, status=response_status.HTTP_200_OK)

            else:
                count = framework_queryset.count()
                # pagination based on limit and skip
                framework_queryset = framework_queryset[skip:skip + limit]
                """framework data"""
                for reg_framework in framework_queryset:
                    # append current framework_id for it's all child regulation
                    related_framework = []
                    if frameworks:
                        related_framework = copy.deepcopy(frameworks)
                    related_framework.append(reg_framework.id)

                    """regulation data"""
                    regulation_doc_qs = RegulatoryFrameworkContentService(
                        organization_id).get_filtered_regulation_queryset(
                        topics, products, materials, regions, is_muted, related_framework, apply_mute_filter=True,
                        status=status)
                    # sort the regulation_dos_qs
                    regulation_doc_qs = RegulatoryFrameworkContentService(
                        organization_id).get_rating_sorted_regulation_doc_qs(regulation_doc_qs, sort_order)
                    # take all the regulation
                    regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]

                    # store all the valid regulation data
                    regulation_list = []
                    for regulation in regulation_doc_qs:
                        # get each regulation object
                        regulation_obj = RegulatoryFrameworkContentService(
                            organization_id).get_tabular_format_regulation_obj(regulation, relevant_topics_ids,
                                                                               is_muted)
                        regulation_list.append(regulation_obj)
                    # get framework object
                    framework_obj = RegulatoryFrameworkContentService(
                        organization_id).get_tabular_format_framework_obj(reg_framework, relevant_topics_ids)
                    # add all the regulations inside the framework
                    framework_obj['regulations'] = regulation_list
                    framework_list.append(framework_obj)
            response = {
                'count': count,
                'results': framework_list
            }
            return Response(response, status=response_status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=response_status.HTTP_500_INTERNAL_SERVER_ERROR)

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

    def get_group_by_response(self, group_by, organization_id, framework_queryset):
        group_by_response = []

        if group_by in ['regions', 'topics']:
            agg_dict = self.get_region_or_topics_group_by_dict(group_by, group_by_field_id=group_by + '.id')
        else:
            agg_dict = self.get_rating_group_by_dict(organization_id)
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
                   query=Q('match', regulatory_framework_rating__organization__id=organization_id))
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

        return group_by_response

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
    def is_name_exists_in_list(list_data, name):
        """
        Return found and index.
        """
        for index, item in enumerate(list_data):
            if item['name'] == name:
                return True, index
        return False, -1
