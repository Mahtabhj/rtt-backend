import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rtttaskManagement.models import TaskHistory
from rttnews.models.models import NewsRelevanceLog
from rttregulation.models.models import RegulationRatingLog, RegulatoryFrameworkRatingLog

logger = logging.getLogger(__name__)


class ImpactRatingTaskHistory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            regulation_id = request.GET.get('regulation_id', None)
            framework_id = request.GET.get('framework_id', None)
            news_id = request.GET.get('news_id', None)
            history_type = request.GET.get('type', 'all').lower()  # all, task, impact_rating
            organization_id = request.user.organization_id
            if not regulation_id and not framework_id and not news_id:
                return Response({"message": "regulation_id AND framework_id AND news_id can not be set empty"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif regulation_id and framework_id and news_id:
                return Response({"message": "regulation_id OR framework_id OR news_id have to send"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif (regulation_id and framework_id) or (framework_id and news_id) or (news_id and regulation_id):
                return Response({"message": "regulation_id OR framework_id OR news_id have to send"},
                                status=status.HTTP_400_BAD_REQUEST)
            impact_rating_news = False
            task_history_qs = TaskHistory.objects.all().order_by('-created')
            if regulation_id:
                task_history_qs = task_history_qs.filter(task__regulations__id=regulation_id)
                impact_rating_qs = RegulationRatingLog.objects.filter(regulation_id=regulation_id,
                                                                      organization_id=organization_id).order_by(
                    '-created')
            elif framework_id:
                task_history_qs = task_history_qs.filter(task__regulatory_frameworks__id=framework_id)
                impact_rating_qs = RegulatoryFrameworkRatingLog.objects.filter(
                    regulatory_framework_id=framework_id, organization_id=organization_id).order_by('-created')
            else:
                task_history_qs = task_history_qs.filter(task__news__id=news_id)
                impact_rating_qs = NewsRelevanceLog.objects.filter(news_id=news_id,
                                                                   organization_id=organization_id).order_by('-created')
                impact_rating_news = True

            response = []
            if history_type in ['all', 'task']:
                response = self.get_task_history_list(task_history_qs)
            if history_type in ['all', 'impact_rating']:
                impact_rating_list = self.get_impact_rating_history(impact_rating_qs, impact_rating_news)
                response.extend(impact_rating_list)

            if history_type == 'all':
                response.sort(key=lambda data: data['date'], reverse=True)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_task_history_list(task_history_qs):
        task_history_list = []
        for task_history in task_history_qs:
            task_history_list.append({
                'id': task_history.id,
                'type': 'task',
                'task': {
                    'id': task_history.task.id,
                    'name': task_history.task.name
                },
                'action_user': {
                    'id': task_history.action_user.id,
                    'username': task_history.action_user.username,
                    'first_name': task_history.action_user.first_name if task_history.action_user.first_name else
                    None,
                    'last_name': task_history.action_user.last_name if task_history.action_user.last_name else None,
                    'avatar': task_history.action_user.avatar.url if task_history.action_user.avatar else None
                },
                'action': task_history.action,
                'action_field': task_history.action_field if task_history.action_field else None,
                'prev_value': task_history.prev_value if task_history.prev_value else None,
                'curr_value': task_history.curr_value if task_history.curr_value else None,
                'date': task_history.created,
                'extra_info': task_history.extra if task_history.extra else None
            })
        return task_history_list

    @staticmethod
    def get_impact_rating_history(impact_rating_qs, impact_rating_news):
        impact_rating_list = []
        for impact_rating in impact_rating_qs:
            action_user_obj = None
            if impact_rating.user:
                action_user_obj = {
                    'id': impact_rating.user.id,
                    'username': impact_rating.user.username,
                    'first_name': impact_rating.user.first_name if impact_rating.user.first_name else None,
                    'last_name': impact_rating.user.last_name if impact_rating.user.last_name else None,
                    'avatar': impact_rating.user.avatar.url if impact_rating.user.avatar else None
                }
            if impact_rating_news:
                rating = impact_rating.relevancy
                prev_rating = impact_rating.prev_relevancy
            else:
                rating = impact_rating.rating
                prev_rating = impact_rating.prev_rating
            impact_rating_list.append({
                'id': impact_rating.id,
                'type': 'impact_rating',
                'action_user': action_user_obj,
                'action': 'changed' if prev_rating else 'created',
                'action_field': 'impact rating',
                'prev_value': prev_rating,
                'curr_value': rating,
                'date': impact_rating.created,
                'extra_info': None
            })
        return impact_rating_list
