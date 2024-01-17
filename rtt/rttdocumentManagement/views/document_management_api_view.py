import copy
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from rttcore.permissions import IsActiveDocumentManagementModule
from rttdocumentManagement.permissions import IsDocManagementEditorSameOrdPermission
from rttdocumentManagement.serializers.serializers import DocumentManagementSerializer, \
    DocumentManagementDetailSerializer, DocumentManagementUpdateSerializer
from rttdocumentManagement.models import DocumentManagement
from rttdocumentManagement.services.doc_management_data_compare_services import DocManagementDataCompareServices
from rttdocumentManagement.services.quota_limit_service import QuotaLimitService
from rttdocumentManagement.services.doc_management_collaborator_services import DocManagementCollaboratorService
from rttdocumentManagement.tasks import doc_management_update_email_notification

logger = logging.getLogger(__name__)


class DocumentManagementViewSet(viewsets.ModelViewSet):
    queryset = DocumentManagement.objects.all()
    serializer_classes = {
        'list': DocumentManagementDetailSerializer,
        'retrieve': DocumentManagementDetailSerializer,
        'update': DocumentManagementUpdateSerializer,
        'partial_update': DocumentManagementUpdateSerializer,
        'create': DocumentManagementDetailSerializer,
    }
    default_serializer_class = DocumentManagementSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, IsActiveDocumentManagementModule,]
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes += [IsDocManagementEditorSameOrdPermission]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1356
        """
        try:
            organization_id = request.user.organization_id
            data = copy.deepcopy(request.data)
            data['uploaded_by'] = request.user.id
            uploaded_attachment_size_in_byte = data['attachment_document'].size
            uploaded_attachment_size_in_mb = uploaded_attachment_size_in_byte * 0.000001

            quota_limit_service = QuotaLimitService(organization_id)
            total_usage = quota_limit_service.get_quota_usage()
            max_quota_for_all_documents, max_quota_for_one_document = quota_limit_service.get_quota_limit()

            available_storage = max_quota_for_all_documents - total_usage

            if uploaded_attachment_size_in_mb > max_quota_for_one_document:
                return Response({'message': "Attachment's size is greater than max quota limit."},
                                status=status.HTTP_400_BAD_REQUEST)
            elif uploaded_attachment_size_in_mb > available_storage:
                return Response({'message': "Attachment's size is greater than available storage limit."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
                document_management_id, collaborator_id = serializer.data['id'], request.user.id
                doc_management_collaborator_service = DocManagementCollaboratorService()
                doc_management_collaborator_service.create_doc_management_collaborator(document_management_id,
                                                                                       collaborator_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1358
        """
        try:
            instance = self.get_object()
            data_compare_services = DocManagementDataCompareServices()
            old_data = data_compare_services.get_old_doc_management_data_dict(instance)
            change_in_attachment_document = False
            if instance.uploaded_by != request.user and request.data.get('attachment_document', None):
                return Response({"message": "This user doesn't have permissions to edit"},
                                status=status.HTTP_403_FORBIDDEN)
            flag = False
            if not request.data.get('regulatory_frameworks', None):
                instance.regulatory_frameworks.clear()
                flag = True
            if not request.data.get('regulations', None):
                instance.regulations.clear()
                flag = True
            if not request.data.get('products', None):
                instance.products.clear()
                flag = True
            if not request.data.get('substances', None):
                instance.substances.clear()
                flag = True
            if not request.data.get('news', None):
                instance.news.clear()
                flag = True
            if flag:
                instance.save()

            if request.data.get('attachment_document', None):
                change_in_attachment_document = True
            data = copy.deepcopy(request.data)
            organization_id = request.user.organization_id
            if request.data.get('attachment_document', None):
                uploaded_attachment_size_in_byte = data['attachment_document'].size
                uploaded_attachment_size_in_mb = uploaded_attachment_size_in_byte * 0.000001

                quota_limit_service = QuotaLimitService(organization_id)
                total_usage = quota_limit_service.get_quota_usage()
                max_quota_for_all_documents, max_quota_for_one_document = quota_limit_service.get_quota_limit()

                available_storage = max_quota_for_all_documents - total_usage

                if uploaded_attachment_size_in_mb > max_quota_for_one_document:
                    return Response({'message': "Attachment's size is greater than max quota limit."},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif uploaded_attachment_size_in_mb > available_storage:
                    return Response({'message': "Attachment's size is greater than available storage limit."},
                                    status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(instance, data=data)
            if serializer.is_valid():
                self.perform_update(serializer)
                document_management_id, collaborator_id = instance.id, request.user.id
                doc_management_collaborator_service = DocManagementCollaboratorService()
                doc_management_collaborator_service.create_doc_management_collaborator(document_management_id,
                                                                                       collaborator_id)
                has_multiple_collaborator = doc_management_collaborator_service.has_multiple_collaborator(
                    document_management_id, collaborator_id)
                if has_multiple_collaborator:
                    new_data = data_compare_services.get_updated_doc_management_data_dict(serializer.data)
                    doc_management_update_email_notification(
                        old_data=old_data, new_data=new_data, editor_id=request.user.id,
                        change_in_attachment_document=change_in_attachment_document)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as pd:
            logger.error(str(pd), exc_info=True)
            return Response({"message": str(pd)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "the document has been deleted"},status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
