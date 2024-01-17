from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from rttcore.services.elasticsearch_service import CelerySignalProcessor
from rttnews.models.models import News, NewsRelevance, NewsAssessmentWorkflow, NewsRelevanceLog
from rttnews.tasks import task_news_assessment_workflow
from rttcore.tasks import substance_m2m_field_task


@receiver(post_save, sender=News)
def news_post_save(sender, instance, **kwargs):
    if instance.status == 's':
        news_id = instance.id
        celery_task = task_news_assessment_workflow.delay(news_id)


@receiver(post_save, sender=NewsRelevanceLog)
def news_relevance_save(sender, instance, **kwargs):
    news_id = instance.news_id
    org_id = instance.organization_id
    try:
        NewsAssessmentWorkflow.objects.filter(news=news_id, organization=org_id).update(status='completed')
    except Exception as ex:
        print(ex)

    '''
    distinct NewsRelevance update or create
    '''
    NewsRelevance.objects.update_or_create(news_id=news_id,
                                           organization_id=org_id,
                                           defaults={
                                               "relevancy": instance.relevancy,
                                               "comment": instance.comment,
                                               "user_id": instance.user_id,
                                           })


@receiver(m2m_changed, sender=News.substances.through, dispatch_uid="substances_news")
def news_substance_m2m_changed(sender, instance, action, pk_set, **kwargs):
    # print('News signal called...', action)
    """
    To sync m2m relations data into elasticsearch, django_elasticsearch_dsl also uses m2m_changed signal.
    Since we are overwrite m2m_changed signal, we have called the the process of elasticsearch syncing here.
    """
    CelerySignalProcessor.handle_m2m_changed_custom(instance, action)

    if action in ('pre_remove', 'post_add'):
        substance_m2m_field_task.delay(instance.id, list(pk_set), action, "substances_news")
