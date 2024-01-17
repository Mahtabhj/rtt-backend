import copy
import logging
from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rttcore.services.system_filter_service import SystemFilterService
from rttregulation.services.regulatory_framework_content_service import RegulatoryFrameworkContentService
from rttregulation.services.relevant_topic_service import RelevantTopicService

logger = logging.getLogger(__name__)


class FrameworkContentGroupByDataTabularFormat(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            topics = request.data.get('topics', None)
            regions = request.data.get('regions', None)
            products = request.data.get('product_categories', None)
            materials = request.data.get('material_categories', None)
            group_by_field = request.data.get('group_by_field', None)  # ['regions', 'topics', 'impact']
            group_by_field_id = request.data.get('group_by_field_id', None)
            is_muted = request.data.get('is_muted', False)
            frameworks = request.data.get('regulatory_frameworks', None)
            regulation_status = request.data.get('status', None)

            sort_order = request.data.get('sort_order', 'desc')  # default sort order is desc by rating
            limit = request.data.get('limit', 10)
            skip = request.data.get('skip', 0)

            if group_by_field not in ['regions', 'topics', 'impact'] or not group_by_field_id >= 0:
                response = {
                    "message": "group_by_field AND group_by_field_id must be sent"
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            self.organization_id = request.user.organization_id
            relevant_topics_ids = RelevantTopicService().get_relevant_topic_id_organization(self.organization_id)
            framework_list = []

            # apply main filter
            framework_doc_qs = RegulatoryFrameworkContentService(
                self.organization_id).get_filtered_regulatory_framework_queryset(
                topics, products, materials, regions, is_muted, frameworks, apply_regulation_mute=True,
                status=regulation_status)
            # filter out using group_by
            framework_doc_qs = self.get_group_filtered_framework_doc_qs(framework_doc_qs, group_by_field,
                                                                        group_by_field_id, is_muted)

            # rating sorted
            framework_doc_qs = RegulatoryFrameworkContentService(
                self.organization_id).get_rating_sorted_regulatory_framework_doc_qs(framework_doc_qs, sort_order)

            count = framework_doc_qs.count()
            # pagination
            framework_doc_qs = framework_doc_qs[skip:skip + limit]

            """framework data"""
            for framework in framework_doc_qs:
                # add current framework_id to its child regulation
                related_frameworks = []
                if frameworks:
                    related_frameworks = copy.deepcopy(frameworks)
                related_frameworks.append(framework.id)
                """regulation data"""
                # apply main filter
                regulation_doc_qs = RegulatoryFrameworkContentService(
                    self.organization_id).get_filtered_regulation_queryset(topics, products, materials, regions,
                                                                           is_muted, related_frameworks,
                                                                           status=regulation_status)
                # filter out using group by
                regulation_doc_qs = self.get_group_filtered_regulation_doc_qs(regulation_doc_qs, group_by_field,
                                                                              group_by_field_id)
                # rating sort
                regulation_doc_qs = RegulatoryFrameworkContentService(
                    self.organization_id).get_rating_sorted_regulation_doc_qs(regulation_doc_qs, sort_order)
                # take all the data
                regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]
                # store all valid regulation
                regulation_list = []
                for regulation in regulation_doc_qs:
                    regulation_obj = RegulatoryFrameworkContentService(
                        self.organization_id).get_tabular_format_regulation_obj(regulation, relevant_topics_ids,
                                                                                is_muted)
                    regulation_list.append(regulation_obj)

                # get framework object
                framework_obj = RegulatoryFrameworkContentService(
                    self.organization_id).get_tabular_format_framework_obj(framework, relevant_topics_ids)
                # add the regulations in side framework object
                framework_obj['regulations'] = regulation_list
                framework_list.append(framework_obj)
            response = {
                'count': count,
                'results': framework_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_group_filtered_framework_doc_qs(self, framework_doc_qs, group_by_field, group_by_field_id, is_muted):

        # filter by region
        if group_by_field == 'regions':
            framework_doc_qs = framework_doc_qs.filter(
                Q('nested',
                  path='regions',
                  query=Q('match', regions__id=group_by_field_id))
            )
        # filter by topic
        elif group_by_field == 'topics':
            framework_doc_qs = framework_doc_qs.filter(
                # filter by topic on framework
                Q('nested',
                  path='topics',
                  query=Q('match', topics__id=group_by_field_id)) |
                # filter by topic on regulation
                Q('nested',
                  path='regulation_regulatory_framework.topics',
                  query=Q('match', regulation_regulatory_framework__topics__id=group_by_field_id))
            )
        else:
            rating_filtered_regulation_id_list = self.get_rating_filtered_regulation_id_list(group_by_field_id,
                                                                                             is_muted)
            # filter by rating zero and null
            if group_by_field_id == 0:
                framework_doc_qs = framework_doc_qs.filter(
                    # apply filter on framework
                    # taking rating which are 0(zero)
                    Q('nested',
                      path='regulatory_framework_rating',
                      query=Q('match', regulatory_framework_rating__organization__id=self.organization_id) &
                        Q('match', regulatory_framework_rating__rating=0)) |
                    # taking rating which are null, cause null value is considered as 0(zero)
                    ~Q('nested',
                       path='regulatory_framework_rating',
                       query=Q('match', regulatory_framework_rating__organization__id=self.organization_id)) |
                    # apply filter on regulation
                    Q('nested',
                      path='regulation_regulatory_framework',
                      query=Q('terms', regulation_regulatory_framework__id=rating_filtered_regulation_id_list))
                )
            # filer by rating greater than or equal to 1 (one)
            else:
                framework_doc_qs = framework_doc_qs.filter(
                    # apply filter on framework
                    Q('nested',
                      path='regulatory_framework_rating',
                      query=Q('match', regulatory_framework_rating__organization__id=self.organization_id) &
                        Q('match', regulatory_framework_rating__rating=group_by_field_id)) |
                    # apply filter on regulation
                    Q('nested',
                      path='regulation_regulatory_framework',
                      query=Q('terms', regulation_regulatory_framework__id=rating_filtered_regulation_id_list))
                )

        return framework_doc_qs

    def get_rating_filtered_regulation_id_list(self, group_by_field_id, is_muted):
        result = []
        regulation_doc_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(self.organization_id,
                                                                                                   is_muted)
        # filter by rating zero and null
        if group_by_field_id == 0:
            regulation_doc_qs = regulation_doc_qs.filter(
                # taking rating which are 0(zero)
                Q('nested',
                  path='regulation_rating',
                  query=Q('match', regulation_rating__organization__id=self.organization_id) &
                    Q('match', regulation_rating__rating=0)) |
                # taking rating which are null, cause null value is considered as 0(zero)
                ~Q('nested',
                   path='regulation_rating',
                   query=Q('match', regulation_rating__organization__id=self.organization_id))
            )
        # filer by rating greater than or equal to 1 (one)
        else:
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='regulation_rating',
                  query=Q('match', regulation_rating__organization__id=self.organization_id) &
                    Q('match', regulation_rating__rating=group_by_field_id))
            )
        regulation_doc_qs = regulation_doc_qs[0:regulation_doc_qs.count()]

        for regulation in regulation_doc_qs:
            result.append(regulation.id)
        return result

    def get_group_filtered_regulation_doc_qs(self, regulation_doc_qs, group_by_field, group_by_field_id):
        # filter by region
        if group_by_field == 'regions':
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('match', regulatory_framework__regions__id=group_by_field_id))
            )
        # filter by topic
        elif group_by_field == 'topics':
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='topics',
                  query=Q('match', topics__id=group_by_field_id))
            )
        # filter by rating
        else:
            if group_by_field_id == 0:
                # filter by rating zero and null
                regulation_doc_qs = regulation_doc_qs.filter(
                    # taking rating which are 0(zero)
                    Q('nested',
                      path='regulation_rating',
                      query=Q('match', regulation_rating__organization__id=self.organization_id) &
                        Q('match', regulation_rating__rating=0)) |
                    # taking rating which are null, cause null value is considered as 0(zero)
                    ~Q('nested',
                       path='regulation_rating',
                       query=Q('match', regulation_rating__organization__id=self.organization_id))
                )
            else:
                # filer by rating greater than or equal to 1 (one)
                regulation_doc_qs = regulation_doc_qs.filter(
                    Q('nested',
                      path='regulation_rating',
                      query=Q('match', regulation_rating__organization__id=self.organization_id) &
                        Q('match', regulation_rating__rating=group_by_field_id))
                )

        return regulation_doc_qs
