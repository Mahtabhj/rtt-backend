import logging
from django.db.models import Q
from rttdocumentManagement.models import DocManagementCollaborator

logger = logging.getLogger(__name__)


class DocManagementCollaboratorService:
    @staticmethod
    def create_doc_management_collaborator(document_management_id, collaborator_id):
        try:
            DocManagementCollaborator.objects.create(document_management_id=document_management_id,
                                                     collaborator_id=collaborator_id)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)

    @staticmethod
    def has_multiple_collaborator(document_management_id, collaborator_id):
        try:
            has_more_multiple_collaborator = DocManagementCollaborator.objects.filter(
                Q(document_management_id=document_management_id) &
                ~Q(collaborator_id=collaborator_id)).exists()
            if has_more_multiple_collaborator:
                return True
            return False
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return False

    @staticmethod
    def get_doc_management_email_notification_receiver(doc_management_id, editor_id):
        results = []
        doc_management_collaborator_qs = DocManagementCollaborator.objects.filter(
            Q(document_management_id=doc_management_id) & ~Q(collaborator_id=editor_id)).select_related('collaborator')
        if doc_management_collaborator_qs.count() > 0:
            for doc_management_collaborator in doc_management_collaborator_qs.all():
                results.append(doc_management_collaborator.collaborator.email)
        return results
