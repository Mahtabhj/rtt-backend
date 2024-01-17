import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsSuperUserOrStaff
from rttnews.models.models import NewsRelevanceLog
from rttregulation.models.models import RegulationRatingLog, RegulatoryFrameworkRatingLog

logger = logging.getLogger(__name__)


class RatingDataGenerator(APIView):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)

    @staticmethod
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'rating_area': openapi.Schema(type=openapi.TYPE_STRING,
                                          enum=['all', 'regulation', 'framework', 'news'])
        }
    ))
    def post(request):
        try:
            response = {'data updated': {'regulation': 0,
                                         'framework': 0,
                                         'news': 0}}

            rating_area = request.data.get('rating_area', 'all')  # all, regulation, framework, news

            '''
            regulation rating log data update
            '''
            updated_qs = []
            if rating_area in ['all', 'regulation']:
                regulation_rating_log_qs = RegulationRatingLog.objects.all().order_by('-id')
                for regulation_rating_log in regulation_rating_log_qs:
                    parent_qs = RegulationRatingLog.objects.filter(
                        organization_id=regulation_rating_log.organization_id,
                        regulation_id=regulation_rating_log.regulation_id,
                        id__lt=regulation_rating_log.id).order_by('-id').first()
                    if parent_qs:
                        regulation_rating_log.prev_rating = parent_qs.rating
                        regulation_rating_log.parent_id = parent_qs.id
                        updated_qs.append(regulation_rating_log)
                        response['data updated']['regulation'] += 1
                RegulationRatingLog.objects.bulk_update(updated_qs, fields=['prev_rating', 'parent'])

            '''
            framework rating log data update
            '''
            updated_qs = []
            if rating_area in ['all', 'framework']:
                framework_rating_log_qs = RegulatoryFrameworkRatingLog.objects.all().order_by('-id')
                for rating_log in framework_rating_log_qs:
                    parent_qs = RegulatoryFrameworkRatingLog.objects.filter(
                        organization_id=rating_log.organization_id,
                        regulatory_framework_id=rating_log.regulatory_framework_id,
                        id__lt=rating_log.id).order_by('-id').first()
                    if parent_qs:
                        rating_log.prev_rating = parent_qs.rating
                        rating_log.parent_id = parent_qs.id
                        updated_qs.append(rating_log)
                        response['data updated']['framework'] += 1
                RegulatoryFrameworkRatingLog.objects.bulk_update(updated_qs, fields=['prev_rating', 'parent'])

            '''
            news rating log data update
            '''
            updated_qs = []
            if rating_area in ['all', 'news']:
                news_rating_log_qs = NewsRelevanceLog.objects.all().order_by('-id')
                for rating_log in news_rating_log_qs:
                    parent_qs = NewsRelevanceLog.objects.filter(
                        organization_id=rating_log.organization_id,
                        news_id=rating_log.news_id,
                        id__lt=rating_log.id).order_by('-id').first()
                    if parent_qs:
                        rating_log.prev_relevancy = parent_qs.relevancy
                        rating_log.parent_id = parent_qs.id
                        updated_qs.append(rating_log)
                        response['data updated']['news'] += 1
                NewsRelevanceLog.objects.bulk_update(updated_qs, fields=['prev_relevancy', 'parent'])
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
