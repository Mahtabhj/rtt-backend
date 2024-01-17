from django.db.models import Q
import datetime
from django.utils import timezone

from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
import traceback

from rtt import celery_app
from django.conf import settings
from rttorganization.models.models import Organization
from rttnews.models.models import NewsAssessmentWorkflow, NewsRelevanceLog, NewsUpdateLogForAssessmentWorkflowRemove
from rttnews.services.news_api_service import NewsApiService
from rttnews.services.news_service import NewsService
from rttcore.services.email_service import send_mail_via_mailjet_template

User = get_user_model()
logger = get_task_logger(__name__)
news_api_service = NewsApiService()
news_service = NewsService()
CELERY_DEFAULT_QUEUE = settings.CELERY_DEFAULT_QUEUE


@celery_app.task(bind=True, queue=CELERY_DEFAULT_QUEUE)
def task_process_news(self, from_date=None):
    try:
        print("process_news task ... ")
        if from_date is None:
            today = datetime.date.today()
            week_ago = today - datetime.timedelta(days=7)
            from_date = str(week_ago)
        print('from date:', from_date)
        res = news_api_service.process_news(from_date)
        logger.info('CeleryTask: news processing from chemical API')
        return res
    except Exception as ex:
        task_id = self.request.id
        users_qs = User.objects.filter(user_celery_task_email_receiver__task_type__in=['fetch_news', 'all'])
        email_to = []
        for user in users_qs:
            email_to.append(user.email)
        subject = f'Chemical News API task failing notification'
        base_url = settings.SITE_BASE_URL
        variables_dict = {
            'date': str(timezone.now().date()),
            'error_message': str(ex),
            'trace_back': str(traceback.format_exc()),
            'task_id': task_id,
            'task_result_url': f'{base_url}backend/admin/django_celery_results/taskresult/?task_id={task_id}'
        }
        template_id = settings.MAILJET_CHEMICAL_NEWS_API_FAILING_NOTIFICATION_TEMPLATE_ID
        send_mail_via_mailjet_template(email_to, template_id, subject, variables_dict)
        raise


@celery_app.task(bind=False, queue=CELERY_DEFAULT_QUEUE)
def task_news_assessment_workflow(news_id):
    print('.......................task_news_assessment_workflow.......................start')
    try:
        organization_document_queryset = news_service.get_relevant_organization_queryset_by_news(news_id)
        organization_ids = []
        for organization_document in organization_document_queryset:
            organization_ids.append(organization_document.id)

        today = timezone.now()
        organization_qs = Organization.objects.filter(id__in=organization_ids,
                                                      organization_subscriptions__start_date__lte=today,
                                                      organization_subscriptions__end_date__gte=today,
                                                      organization_subscriptions__type__live_assessment=True).distinct()
        assessment_workflow_organization_ids = []
        for org_qs in organization_qs:

            news_relevance_log_exist = NewsRelevanceLog.objects.filter(Q(news_id=news_id) &
                                                                       Q(organization_id=org_qs.id)).exists()

            if not news_relevance_log_exist:
                obj, created = NewsAssessmentWorkflow.objects.get_or_create(
                    news_id=news_id,
                    organization_id=org_qs.id,
                    # defaults={'status': 'to_be_assessed'},
                )
                assessment_workflow_organization_ids.append(org_qs.id)

        return {'message': 'task_news_assessment_workflow has executed successfully',
                'news_id': news_id,
                'relevant_organization_ids': organization_ids,
                'assessment_workflow_organization_ids': assessment_workflow_organization_ids
                }
    except Exception as ex:
        print(ex)
        raise


@celery_app.task(bind=False, queue=CELERY_DEFAULT_QUEUE)
def task_remove_existing_irrelevant_news_assessment_workflow():
    print('.......................task_remove_existing_irrelevant_news_assessment_workflow.......................start')
    try:
        visited_news = {}
        news_log_for_workflow_remove_qs = NewsUpdateLogForAssessmentWorkflowRemove.objects.filter(active=True)
        for news_log_for_workflow_remove in news_log_for_workflow_remove_qs:
            news_id = news_log_for_workflow_remove.news_id
            news_log_for_workflow_remove.active = False
            news_log_for_workflow_remove.save()
            if str(news_id) not in visited_news:
                visited_news[str(news_id)] = True
                organization_doc_qs = NewsService().get_relevant_organization_queryset_by_news(news_id)
                organization_doc_qs = organization_doc_qs[0:organization_doc_qs.count()]
                relevant_org_id_list = []
                for org in organization_doc_qs:
                    relevant_org_id_list.append(org.id)
                NewsAssessmentWorkflow.objects.filter(Q(news_id=news_id) & Q(status__exact='to_be_assessed') &
                                                      ~Q(organization_id__in=relevant_org_id_list)).delete()
        return {'message': 'task_remove_existing_irrelevant_news_assessment_workflow has executed successfully'}
    except Exception as ex:
        logger.error(str(ex), exc_info=True)
    return {'message': 'server error'}

