import logging
import copy
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from rttcore.permissions import IsActiveDocumentManagementModule
from rttdocumentManagement.permissions import HasDocManagementCommentEditPermission
from rttdocumentManagement.models import DocumentManagementComment, DocumentManagement
from rttdocumentManagement.serializers.serializers import DocumentManagementCommentSerializer, \
    DocumentManagementCommentUpdateSerializer, DocumentManagementCommentDefaultSerializer
from rttdocumentManagement.services.doc_management_collaborator_services import DocManagementCollaboratorService
from rttdocumentManagement.tasks import doc_management_comment_email_notification

User = get_user_model()
logger = logging.getLogger(__name__)


class DocumentManagementCommentViewSet(ModelViewSet):
    queryset = DocumentManagementComment.objects.all()
    serializer_classes = {
        'list': DocumentManagementCommentDefaultSerializer,
        'retrieve': DocumentManagementCommentSerializer,
        'create': DocumentManagementCommentSerializer,
        'update': DocumentManagementCommentUpdateSerializer,
        'partial_update': DocumentManagementCommentUpdateSerializer,
        'get_related_comments': DocumentManagementCommentSerializer,
    }
    default_serializer_class = DocumentManagementCommentDefaultSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        queryset = self.filter_queryset(self.queryset)
        return queryset

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated, IsActiveDocumentManagementModule,]
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes += [HasDocManagementCommentEditPermission]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            limit = int(self.request.GET.get('limit', 10))
            skip = int(self.request.GET.get('skip', 0))
            queryset_count = queryset.count()
            queryset = queryset[skip: skip + limit]
            serializer = self.get_serializer(instance=queryset, many=True)
            response = {
                'count': queryset_count,
                'results': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance=instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            data = copy.deepcopy(request.data)
            doc_management_id = data['document_management']
            doc_management_obj = DocumentManagement.objects.filter(id=doc_management_id).first()
            doc_management = {
                'id': doc_management_obj.id,
                'name': doc_management_obj.name,
            }
            editor_id = request.user.id
            new_doc_comment = data['comment_text']
            data['commented_by'] = request.user.id
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
                document_management_id, collaborator_id = request.data['document_management'], request.user.id
                DocManagementCollaboratorService().create_doc_management_collaborator(document_management_id,
                                                                                      collaborator_id)
                doc_management_comment_email_notification(doc_management, editor_id, old_doc_comment=None,
                                                          new_doc_comment=new_doc_comment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            doc_management = {
                'id': instance.document_management.id,
                'name': instance.document_management.name,
            }
            editor_id = instance.commented_by_id
            old_doc_comment, new_doc_comment = instance.comment_text, request.data.get('comment_text', '')
            data = copy.deepcopy(request.data)
            data['edited'] = timezone.now()
            serializer = self.get_serializer(instance=instance, data=data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                doc_management_comment_email_notification(doc_management, editor_id, old_doc_comment, new_doc_comment)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as pd:
            logger.error(str(pd), exc_info=True)
            return Response({"message": str(pd)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['get'], detail=False, url_path='get-related-comments')
    def get_related_comments(self, request, *args, **kwargs):
        try:
            doc_management_id = request.GET.get('doc_id', None)
            if not doc_management_id:
                return Response({"message": "document_management ID must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = self.get_queryset().filter(document_management_id=doc_management_id)
            queryset_count = queryset.count()
            limit = int(request.GET.get('limit', 10))
            skip = int(request.GET.get('skip', 0))
            queryset = queryset[skip:skip + limit]
            serializer = self.get_serializer(instance=queryset, many=True)
            response = {
                'count': queryset_count,
                'results': serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
