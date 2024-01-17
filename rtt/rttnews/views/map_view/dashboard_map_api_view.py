import logging
import pytz
from datetime import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.services.dashboard_services import DashboardService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttcore.services.id_search_service import IdSearchService

logger = logging.getLogger(__name__)
utc = pytz.UTC


class DashBoardMapAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-810
        """
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
                'frameworks': request.data.get('frameworks', None)
            }
            region_results = []
            organization_id = request.user.organization_id
            filters_value_for_total_len = {
                'from_date': request.data.get('from_date', None),
                'to_date': request.data.get('to_date', None),
                'organization_id': organization_id,
            }
            dashboard_service = DashboardService()
            related_milestones_ids = RelevantRegulationService().get_relevant_milestone_id_organization(
                organization_id)
            queryset_news = []
            if dashboard_service.is_return_data(filters, 'news'):
                queryset_news = dashboard_service.get_filtered_news_queryset(filters, organization_id)
                queryset_news = queryset_news[0:queryset_news.count()]
            queryset_regulation = []
            if dashboard_service.is_return_data(filters, 'regulations'):
                queryset_regulation = dashboard_service.get_filtered_regulation_queryset(filters, organization_id)
                queryset_regulation = queryset_regulation[0:queryset_regulation.count()]
            queryset_regulatory = []
            if dashboard_service.is_return_data(filters, 'frameworks'):
                queryset_regulatory = dashboard_service.get_filtered_regulatory_framework_queryset(filters,
                                                                                                   organization_id)
                queryset_regulatory = queryset_regulatory[0:queryset_regulatory.count()]
            for news in queryset_news:
                self.prepare_data(news.regions, region_results, 'news', news, filters_value_for_total_len)
            for regulation in queryset_regulation:
                self.prepare_data(regulation.regulatory_framework.regions, region_results, 'regulations', regulation,
                                  filters_value_for_total_len, related_milestones_ids)
            for regulatory in queryset_regulatory:
                self.prepare_data(regulatory.regions, region_results, 'frameworks', regulatory,
                                  filters_value_for_total_len, related_milestones_ids)
            return Response({'regions': region_results}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def is_id_exists_in_list(list_data, id):
        """
        Return found and index.
        """
        for index, item in enumerate(list_data):
            if item['id'] == id:
                return True, index
        return False, -1

    def prepare_data(self, source_data, result_data, area, area_obj, filters_value_for_total_len,
                     related_milestones_ids=None):
        from_date = datetime.strptime(filters_value_for_total_len['from_date'], "%Y-%m-%d").replace(
            tzinfo=utc) if filters_value_for_total_len['from_date'] else None
        to_date = datetime.strptime(filters_value_for_total_len['to_date'], "%Y-%m-%d").replace(
            tzinfo=utc, hour=23) if filters_value_for_total_len['to_date'] else None
        for data in source_data:
            found, index = self.is_id_exists_in_list(result_data, data.id)
            if found:
                result_data[index][area]['selected_ids'].append(area_obj.id)
                if area == 'news':
                    result_data[index][area]['total_length'] += 1

                if area == 'regulations':
                    queryset_regulation_total_len = self.get_regulation_total_len(area_obj, from_date, to_date,
                                                                                  related_milestones_ids)
                    result_data[index][area]['total_length'] += queryset_regulation_total_len
                elif area == 'frameworks':
                    queryset_regulatory_total_len = self.get_framework_total_len(area_obj, from_date, to_date,
                                                                                 related_milestones_ids)
                    result_data[index][area]['total_length'] += queryset_regulatory_total_len
            else:
                queryset_regulation_total_len = 0
                queryset_regulatory_total_len = 0
                queryset_news_total_len = 1 if area == 'news' else 0
                if area == 'regulations':
                    queryset_regulation_total_len = self.get_regulation_total_len(area_obj, from_date, to_date,
                                                                                  related_milestones_ids)
                elif area == 'frameworks':
                    queryset_regulatory_total_len = self.get_framework_total_len(area_obj, from_date, to_date,
                                                                                 related_milestones_ids)
                temp = {
                    'id': data.id,
                    'title': data.name,
                    'country_code': data.country_code,
                    'latitude': data.latitude,
                    'longitude': data.longitude,
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

                temp[area]['selected_ids'].append(area_obj.id)
                result_data.append(temp)

    @staticmethod
    def get_framework_total_len(regulatory_obj, from_date, to_date, related_milestones_ids):
        framework_total_len = 0
        for milestone in regulatory_obj.regulatory_framework_milestone:
            if IdSearchService().does_id_exit_in_sorted_list(related_milestones_ids, milestone.id):
                if from_date and to_date:
                    if from_date <= milestone.from_date <= to_date:
                        framework_total_len += 1
                else:
                    framework_total_len += 1
        return framework_total_len

    @staticmethod
    def get_regulation_total_len(regulation_obj, from_date, to_date, related_milestones_ids):
        regulation_total_len = 0
        for milestone in regulation_obj.regulation_milestone:
            if IdSearchService().does_id_exit_in_sorted_list(related_milestones_ids, milestone.id):
                if from_date and to_date:
                    if milestone.from_date and from_date <= milestone.from_date <= to_date:
                        regulation_total_len += 1
                else:
                    regulation_total_len += 1
        return regulation_total_len
