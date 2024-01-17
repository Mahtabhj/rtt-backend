from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from rttcore.services.elasticsearch_service import CelerySignalProcessor
from rttregulation.models.models import RegulationRatingLog, RegulationRating, RegulatoryFrameworkRatingLog, \
    RegulatoryFrameworkRating, RegulatoryFramework, RegulationMilestone, Regulation
from rttcore.tasks import substance_m2m_field_task


@receiver(post_save, sender=RegulationRatingLog)
def regulation_rating_save(sender, instance, **kwargs):
    """
    distinct RegulationRating update or create
    """
    RegulationRating.objects.update_or_create(regulation_id=instance.regulation_id,
                                              organization_id=instance.organization_id,
                                              defaults={
                                                  "rating": instance.rating,
                                                  "comment": instance.comment,
                                                  "user_id": instance.user_id,
                                              })


@receiver(post_save, sender=RegulatoryFrameworkRatingLog)
def regulatory_framework_rating_save(sender, instance, **kwargs):
    """
    distinct RegulatoryFrameworkRating update or create
    """
    RegulatoryFrameworkRating.objects.update_or_create(regulatory_framework_id=instance.regulatory_framework_id,
                                                       organization_id=instance.organization_id,
                                                       defaults={
                                                           "rating": instance.rating,
                                                           "comment": instance.comment,
                                                           "user_id": instance.user_id,
                                                       })


'''
m2m_changed signal docs
https://docs.djangoproject.com/en/3.2/ref/signals/#m2m-changed
'''


@receiver(m2m_changed, sender=RegulatoryFramework.substances.through, dispatch_uid="substances_regulatory_framework")
def regulatory_framework_substance_m2m_changed(sender, instance, action, pk_set, **kwargs):
    # print('RegulatoryFramework signal called...', action)
    """
    To sync m2m relations data into elasticsearch, django_elasticsearch_dsl also uses m2m_changed signal.
    Since we are overwrite m2m_changed signal, we have called the the process of elasticsearch syncing here.
    """
    CelerySignalProcessor.handle_m2m_changed_custom(instance, action)
    '''
    for relation date store
    '''
    if action in ('pre_remove', 'post_add'):
        substance_m2m_field_task.delay(instance.id, list(pk_set), action, "substances_regulatory_framework")


@receiver(m2m_changed, sender=Regulation.substances.through, dispatch_uid="substances_regulation")
def regulation_substance_m2m_changed(sender, instance, action, pk_set, **kwargs):
    # print('Regulation signal called...', action)
    """
    To sync m2m relations data into elasticsearch, django_elasticsearch_dsl also uses m2m_changed signal.
    Since we are overwrite m2m_changed signal, we have called the the process of elasticsearch syncing here.
    """
    CelerySignalProcessor.handle_m2m_changed_custom(instance, action)

    '''
    for relation date store
    '''
    if action in ('pre_remove', 'post_add'):
        substance_m2m_field_task.delay(instance.id, list(pk_set), action, "substances_regulation")


@receiver(m2m_changed, sender=RegulationMilestone.substances.through, dispatch_uid="substances_regulation_milestone")
def regulation_milestone_substance_m2m_changed(sender, instance, action, pk_set, **kwargs):
    # print('RegulationMilestone signal called...', action)
    """
    To sync m2m relations data into elasticsearch, django_elasticsearch_dsl also uses m2m_changed signal.
    Since we are overwrite m2m_changed signal, we have called the the process of elasticsearch syncing here.
    """
    CelerySignalProcessor.handle_m2m_changed_custom(instance, action)

    '''
    for relation date store 
    '''
    if action in ('pre_remove', 'post_add'):
        substance_m2m_field_task.delay(instance.id, list(pk_set), action, "substances_regulation_milestone")
