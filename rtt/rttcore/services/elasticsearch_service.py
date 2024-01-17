from django.db import transaction
from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl.signals import RealTimeSignalProcessor
from rttcore.tasks import handle_es_save


class CelerySignalProcessor(RealTimeSignalProcessor):
    """Celery signal processor.
    Allows automatic updates on the index as delayed background tasks using
    Celery.
    NB: This cannot process deletes as background tasks.
    By the time the Celery worker would pick up the delete job, the
    model instance would already deleted.
    """

    def handle_save(self, sender, instance, **kwargs):
        """Handle save.

        Given an individual model instance, update the object in the index.
        Update the related objects either.
        """
        print('handle_save called')
        app_label = instance._meta.app_label
        model_name = instance._meta.model_name
        transaction.on_commit(lambda: handle_es_save.delay(instance.pk, app_label, model_name))

    @staticmethod
    def handle_m2m_changed_custom(instance, action):
        if action in ('post_add', 'post_remove', 'post_clear'):
            app_label = instance._meta.app_label
            model_name = instance._meta.model_name
            transaction.on_commit(lambda: handle_es_save.delay(instance.pk, app_label, model_name))
        elif action in ('pre_remove', 'pre_clear'):
            registry.delete_related(instance)

    # def handle_pre_delete(self, sender, instance, **kwargs):
    #     """Handle removing of instance object from related models instance.
    #     We need to do this before the real delete otherwise the relation
    #     doesn't exists anymore and we can't get the related models instance.
    #     """
    #
    #     app_label = instance._meta.app_label
    #     model_name = instance._meta.model_name
    #     handle_es_pre_delete.delay(instance.pk, app_label, model_name)
    #
    # def handle_delete(self, sender, instance, **kwargs):
    #     """Handle delete.
    #
    #     Given an individual model instance, delete the object from index.
    #     """
    #
    #     app_label = instance._meta.app_label
    #     model_name = instance._meta.model_name
    #     handle_es_delete.delay(instance.pk, app_label, model_name)
