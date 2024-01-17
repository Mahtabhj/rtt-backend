from django.apps import apps
from django_elasticsearch_dsl.registries import registry
from rtt import celery_app
from django.conf import settings
from rttregulation.models.models import SubstanceRegulatoryFramework, SubstanceRegulation, SubstanceRegulationMilestone
from rttnews.models.models import SubstanceNews

CELERY_ES_QUEUE = settings.CELERY_ES_QUEUE


@celery_app.task(ignore_result=True, queue=CELERY_ES_QUEUE)
def handle_es_save(pk, app_label, model_name):
    print('celery handle_es_save...', pk, model_name)
    sender = apps.get_model(app_label, model_name)
    instance = sender.objects.get(pk=pk)
    registry.update(instance)
    registry.update_related(instance)


# @celery_app.task(ignore_result=True)
# def handle_es_pre_delete(pk, app_label, model_name):
#     sender = apps.get_model(app_label, model_name)
#     instance = sender.objects.get(pk=pk)
#     registry.delete_related(instance)
#
#
# @celery_app.task(ignore_result=True)
# def handle_es_delete(pk, app_label, model_name):
#     sender = apps.get_model(app_label, model_name)
#     instance = sender.objects.get(pk=pk)
#     registry.delete(instance, raise_on_error=False)


@celery_app.task(ignore_result=True, queue=CELERY_ES_QUEUE)
def substance_m2m_field_task(obj_id, substance_pk_list, action, obj_type):
    print(f'[Celery Task: substance_m2m_field_task] {action} is called ------> for {obj_type}')
    substances_ids = substance_pk_list
    if obj_type == 'substances_news':
        if action == 'pre_remove':
            # print(f'{action} in {obj_type}')
            deleted_data = SubstanceNews.objects.filter(news_id=obj_id,
                                                        substance_id__in=substances_ids).delete()
        if action == 'post_add':
            # print(f'{action} in {obj_type}')
            for substance_id in substances_ids:
                SubstanceNews.objects.update_or_create(news_id=obj_id,
                                                       substance_id=substance_id)
    elif obj_type == 'substances_regulatory_framework':
        if action == 'pre_remove':
            # print(f'{action} in {obj_type}')
            deleted_data = SubstanceRegulatoryFramework.objects.filter(regulatory_framework_id=obj_id,
                                                                       substance_id__in=substances_ids).delete()
        if action == 'post_add':
            for substance_id in substances_ids:
                # print(f'{action} in {obj_type}')
                SubstanceRegulatoryFramework.objects.update_or_create(regulatory_framework_id=obj_id,
                                                                      substance_id=substance_id)
    elif obj_type == 'substances_regulation':
        if action == 'pre_remove':
            # print(f'{action} in {obj_type}')
            deleted_data = SubstanceRegulation.objects.filter(regulation_id=obj_id,
                                                              substance_id__in=substances_ids).delete()
        if action == 'post_add':
            # print(f'{action} in {obj_type}')
            for substance_id in substances_ids:
                SubstanceRegulation.objects.update_or_create(regulation_id=obj_id,
                                                             substance_id=substance_id)
    elif obj_type == 'substances_regulation_milestone':
        if action == 'pre_remove':
            # print(f'{action} in {obj_type}')
            deleted_data = SubstanceRegulationMilestone.objects.filter(regulation_milestone_id=obj_id,
                                                                       substance_id__in=substances_ids).delete()
        if action == 'post_add':
            # print(f'{action} in {obj_type}')
            for substance_id in substances_ids:
                SubstanceRegulationMilestone.objects.update_or_create(regulation_milestone_id=obj_id,
                                                                      substance_id=substance_id)
