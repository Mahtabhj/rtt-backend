from collections import defaultdict
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from elasticsearch_dsl import Q

from rttcore.permissions import IsActiveSubstanceModule
from rttcore.services.system_filter_service import SystemFilterService


class SubstanceTimeLine(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    def get(self, request, substance_id):
        try:
            substance_id = int(substance_id)
            organization_id = request.user.organization_id
            created_date_list = []
            created_milestone_list = set()
            response = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: []))))
            """
            news data
            """
            queryset_news = SystemFilterService().get_system_filtered_news_document_queryset(organization_id).filter(
                # news tagged to substance
                Q('nested',
                  path='substances',
                  query=Q('match', substances__id=substance_id)))
            queryset_news = queryset_news[0:queryset_news.count()]
            for news in queryset_news:
                date = news.pub_date
                self.assign_data(date, created_date_list, response, data_name='news', data_id=news.id)
            """
            framework data
            """
            queryset_framework = SystemFilterService().get_system_filtered_regulatory_framework_queryset(
                organization_id).filter(
                # milestones of regulatory frameworks to which the milestone is tagged
                Q('nested',
                  path='substances',
                  query=Q('match', substances__id=substance_id))).filter(
                # making sure every framework has milestone(s)
                Q('nested',
                  path='regulatory_framework_milestone',
                  query=Q('exists', field="regulatory_framework_milestone.id"))
            )
            queryset_framework = queryset_framework[0:queryset_framework.count()]
            for framework in queryset_framework:
                for milestone in framework.regulatory_framework_milestone:
                    date = milestone.from_date
                    self.assign_data(date, created_date_list, response, data_name='frameworks', data_id=framework.id)
                    created_milestone_list.add(milestone.id)
            """
            regulation data
            """
            queryset_regulation = SystemFilterService().get_system_filtered_regulation_document_queryset(
                organization_id).filter(
                # milestones of regulation to which the substance is tagged
                Q('nested',
                  path='substances',
                  query=Q('match', substances__id=substance_id))).filter(
                # making sure every regulation has milestone(s)
                Q('nested',
                  path='regulation_milestone',
                  query=Q('exists', field="regulation_milestone.id"))
            )
            queryset_regulation = queryset_regulation[0:queryset_regulation.count()]
            for regulation in queryset_regulation:
                for milestone in regulation.regulation_milestone:
                    date = milestone.from_date
                    self.assign_data(date, created_date_list, response, data_name='regulations', data_id=regulation.id)
                    created_milestone_list.add(milestone.id)
            """
            framework via milestone or regulation via milestone
            """
            created_milestone_list = list(created_milestone_list)
            milestone_doc_qs = SystemFilterService().get_system_filtered_milestone_document_queryset(
                organization_id).filter(
                # milestones to which the substance is tagged
                Q('nested',
                  path='substances',
                  query=Q('match', substances__id=substance_id))
            ).filter(
                # making sure milestone is not already added previously
                ~Q('terms', id=created_milestone_list)
            )
            milestone_doc_qs = milestone_doc_qs[0:milestone_doc_qs.count()]
            for milestone in milestone_doc_qs:
                date = milestone.from_date
                if milestone.regulatory_framework:
                    framework_id = milestone.regulatory_framework.id
                    self.assign_data(date, created_date_list, response, data_name='frameworks', data_id=framework_id)
                if milestone.regulation:
                    regulation_id = milestone.regulation.id
                    self.assign_data(date, created_date_list, response, data_name='regulations', data_id=regulation_id)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def assign_data(date, created_date_list, response, data_name, data_id):
        if date not in created_date_list:
            response[str(date.year)][str(date.month)][str(date.day)]['regulations'] = []
            response[str(date.year)][str(date.month)][str(date.day)]['news'] = []
            response[str(date.year)][str(date.month)][str(date.day)]['frameworks'] = []
            created_date_list.append(date)
        response[str(date.year)][str(date.month)][str(date.day)][data_name].append(data_id)
