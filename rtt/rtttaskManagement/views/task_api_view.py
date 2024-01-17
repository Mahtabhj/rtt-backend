import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings

from rttcore.permissions import IsActiveTaskManagementModule
from django.contrib.auth import get_user_model
from rtttaskManagement.serializers.serializers import TaskSerializer, TaskUpdateSerializer, TaskDetailsSerializer
from rtttaskManagement.models import Task, TaskEditor, TaskHistory
from rttcore.services.email_service import send_mail_via_mailjet_template
from rtttaskManagement.tasks import task_management_update_email_notification

logger = logging.getLogger(__name__)
User = get_user_model()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().prefetch_related('products', 'regulatory_frameworks', 'regulations').select_related(
        'created_by', 'assignee')
    serializer_classes = {
        'retrieve': TaskDetailsSerializer,
        'update': TaskUpdateSerializer,
        'partial_update': TaskUpdateSerializer,
    }
    default_serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsActiveTaskManagementModule, )
    lookup_field = 'id'

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            task_id = serializer.data.get('id', None)
            self.set_user_to_task_editor(task_id, user_id=request.user.id)
            self.task_management_create_email_notification(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.set_user_to_task_editor(task_id=instance.id, user_id=request.user.id)
        old_data = self.get_old_data(instance)
        self.perform_update(serializer)
        task_management_update_email_notification.delay(old_data, serializer.data, request.user.id)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @staticmethod
    def set_user_to_task_editor(task_id, user_id):
        try:
            TaskEditor.objects.create(task_id=task_id, editor_id=user_id)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)

    @staticmethod
    def get_old_data(task_instance):
        assignee = None
        if task_instance.assignee:
            assignee = {
                'id': task_instance.assignee.id,
                'first_name': task_instance.assignee.first_name if task_instance.assignee.first_name else '',
                'last_name': task_instance.assignee.last_name if task_instance.assignee.last_name else '',
                'email': task_instance.assignee.email,
                'username': task_instance.assignee.username,
            }
        result = {
            'id': task_instance.id,
            'name': task_instance.name,
            'description': task_instance.description if task_instance.description else None,
            'status': task_instance.status,
            'created_by': {
                'id': task_instance.created_by.id,
                'email': task_instance.created_by.email
            },
            'assignee': assignee,
            'products': [{'id': product.id, 'name': product.name} for product in task_instance.products.all()],
            'due_date': str(task_instance.due_date) if task_instance.due_date else None,
            'is_archive': task_instance.is_archive,
            'regulations': [{'id': regulation.id, 'name': regulation.name} for regulation in task_instance.regulations.all()],
            'regulatory_frameworks': [{'id': framework.id, 'name': framework.name} for framework in task_instance.regulatory_frameworks.all()],
            'news': [{'id': news.id, 'title': news.title} for news in task_instance.news.all()],
            'substances': [{'id': substance.id, 'name': substance.name, 'ec_no': substance.ec_no,
                            'cas_no': substance.cas_no} for substance in task_instance.substances.all()],
        }
        return result

    @staticmethod
    def task_management_create_email_notification(task_data):
        try:
            assignee_id = task_data.get('assignee', None)
            reporter_id = task_data.get('created_by', None)
            # storing tasks logs
            TaskHistory.objects.create(task_id=task_data['id'], action_user_id=reporter_id, action='created',
                                       action_field='new task', curr_value=task_data['name'], extra=task_data)
            # ------------------end storing tasks logs------------------
            if assignee_id and assignee_id != reporter_id:
                assignee = User.objects.filter(id=assignee_id).first()
                email_to = assignee.email
                task_id = task_data.get('id', None)
                name = task_data.get('name', None)
                subject = f'New task: {name}'
                reporter = User.objects.filter(id=reporter_id).first()
                description = task_data.get('description', None)
                due_date = task_data.get('due_date', None)
                base_url = settings.SITE_BASE_URL

                reporter_name = reporter.username
                if reporter.first_name:
                    reporter_name = reporter.first_name
                if reporter.last_name and reporter.first_name:
                    reporter_name = f'{reporter_name} {reporter.last_name}'

                assignee_name = assignee.username
                if assignee.first_name:
                    assignee_name = assignee.first_name
                if assignee.last_name and assignee.first_name:
                    assignee_name = f'{assignee_name} {assignee.last_name}'

                variables_dict = {
                    'reporter': reporter_name,
                    'assignee': assignee_name,
                    'has_description': True if description else False,
                    'description': description if description else '',
                    'due_date': due_date[:10] if due_date else 'Not set',
                    'view_task_url': f'{base_url}tasks/task/{task_id}'
                }
                template_id = settings.MAILJET_TASK_CREATE_NOTIFICATION_TEMPLATE_ID
                send_mail_via_mailjet_template(email_to, template_id, subject, variables_dict)

        except Exception as ex:
            logger.error(str(ex), exc_info=True)
