from datetime import datetime

from rttdocumentManagement.models import DocumentManagement
from rttorganization.models.models import Subscription


class QuotaLimitService:
    def __init__(self, organization_id):
        self.organization_id = organization_id

    def get_quota_usage(self):
        document_qs = DocumentManagement.objects.filter(uploaded_by__organization=self.organization_id)
        size_of_all_documents = 0
        for document in document_qs:
            size_in_byte = document.attachment_document.size if document.attachment_document else 0
            size_in_mb = size_in_byte * 0.000001
            size_of_all_documents += size_in_mb
        return size_of_all_documents

    def get_quota_limit(self):
        current_time = datetime.now()
        subscription_qs = Subscription.objects.filter(
            organization=self.organization_id, start_date__lte=current_time, end_date__gte=current_time,
            type__is_active_document_module=True).order_by('-end_date')
        if len(list(subscription_qs)) == 0:
            return 0, 0
        subscription_type = list(subscription_qs)[0].type

        max_quota_for_all_documents = subscription_type.max_quota_for_all_documents
        max_quota_for_one_document = subscription_type.max_quota_for_one_document

        return max_quota_for_all_documents, max_quota_for_one_document
