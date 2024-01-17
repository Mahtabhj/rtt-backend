import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

from django.contrib.auth import get_user_model

from django.conf import settings
from rtttaskManagement.serializers.serializers import TaskCommentSerializer, TaskCommentUpdateSerializer
from rtttaskManagement.models import Task, TaskComment, TaskEditor
from rttcore.services.email_service import send_mail_via_mailjet_template


logger = logging.getLogger(__name__)
User = get_user_model()


class TaskCommentViewSet(viewsets.ModelViewSet):
    """
    doc: https://chemycal.atlassian.net/browse/RTT-946
    """
    queryset = TaskComment.objects.all()
    serializer_classes = {
        'retrieve': TaskCommentSerializer,
        'update': TaskCommentUpdateSerializer,
        'partial_update': TaskCommentUpdateSerializer,
    }
    default_serializer_class = TaskCommentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def list(self, request, *args, **kwargs):
        task_id = request.GET.get('task_id', None)

        if not task_id:
            return Response({"message": "task_id must be sent"},
                            status=status.HTTP_400_BAD_REQUEST)
        limit = int(request.GET.get('limit', 4))
        skip = int(request.GET.get('skip', 0))

        task_comment_qs = TaskComment.objects.filter(task_id=task_id)
        response = {
            'count': task_comment_qs.count(),
            'results': []
        }
        task_comment_qs = task_comment_qs[skip:skip + limit]

        for task_comment in task_comment_qs:
            commented_by_obj = {
                'id': task_comment.commented_by.id,
                'first_name': task_comment.commented_by.first_name if task_comment.commented_by.first_name else None,
                'last_name': task_comment.commented_by.last_name if task_comment.commented_by.last_name else None,
                'username': task_comment.commented_by.username,
                'avatar': task_comment.commented_by.avatar.url if task_comment.commented_by.avatar else None
            }
            response['results'].append({
                'id': task_comment.id,
                'comment_text': task_comment.comment_text,
                'created': task_comment.created,
                'modified': task_comment.modified,
                'edited': task_comment.edited,
                'commented_by': commented_by_obj,
                'has_write_access': True if task_comment.commented_by_id == request.user.id else False
            })

        return Response(response, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['commented_by'] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            task_id = serializer.data['task']
            self.set_user_to_task_editor(task_id, user_id=request.user.id)
            self.send_comment_email_notification(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = request.user.id

        if user_id != instance.commented_by.id:
            return Response({"message": "Only Commenter has the permission to edit"},
                            status=status.HTTP_403_FORBIDDEN)
        if request.data.get('comment_text', None):
            if instance.comment_text != request.data.get('comment_text'):
                request.data['edited'] = timezone.now()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.commented_by.id != request.user.id:
                return Response({'message': 'you do not have permission to delete!'}, status=status.HTTP_403_FORBIDDEN)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def set_user_to_task_editor(task_id, user_id):
        try:
            TaskEditor.objects.create(task_id=task_id, editor_id=user_id)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)

    @staticmethod
    def send_comment_email_notification(comment_data):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-947
        """
        try:
            base_url = settings.SITE_BASE_URL
            variables_dict = {
                'task_updated': '',
                'has_title_diff': False,
                'has_assignee_diff': False,
                'has_status_diff': False,
                'has_due_date_diff': False,
                'has_description_diff': False,
                'has_product_diff': False,
                'has_archive_diff': False,
                'has_new_comment': True,
                'new_comment': '',
                'view_task_url': f"{base_url}tasks/task/{comment_data['task']}"
            }
            task_obj = Task.objects.filter(id=comment_data['task']).select_related('assignee').first()
            subject = f'Task update: {task_obj.name}'
            variables_dict['new_comment'] = comment_data['comment_text']
            today = timezone.now()
            commented_by_obj = User.objects.filter(id=comment_data['commented_by']['id']).first()
            # generate name, who has created the comment
            name = ''
            if commented_by_obj.first_name:
                name += commented_by_obj.first_name
                if commented_by_obj.last_name:
                    name = name + ' ' + commented_by_obj.last_name
            else:
                name = commented_by_obj.username
            variables_dict['task_updated'] = f'{name} added a comment ({str(today)[:10]})'

            email_to = []
            # send mail to the task_assignee if he is not the creator of tha comment
            if task_obj.assignee and task_obj.assignee.id != comment_data['commented_by']['id']:
                email_to.append(task_obj.assignee.email)

            # send email, who are in the taskEditor list except the comment creator
            task_editor_qs = TaskEditor.objects.filter(
                Q(task_id=comment_data['task']) & ~Q(editor_id=comment_data['commented_by']['id'])).select_related(
                'editor')
            for task_editor in task_editor_qs.all():
                email_to.append(task_editor.editor.email)

            template_id = settings.MAILJET_TASK_UPDATE_NOTIFICATION_TEMPLATE_ID
            send_mail_via_mailjet_template(email_to, template_id, subject, variables_dict)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
