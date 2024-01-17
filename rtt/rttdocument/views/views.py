from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rttdocument.filters import DocumentFilter
from rttdocument.models.models import DocumentType, Document, Help
from rttdocument.serializers import documets_serializers


class DocumentTypeViewSet(ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = documets_serializers.DocumentTypeSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'id'

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(documets_serializers.DocumentTypeSerializer(page, many=True).data)
        else:
            serializer = documets_serializers.DocumentTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DocumentViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_classes = {
        'list': documets_serializers.DocumentDetailSerializer,
        'retrieve': documets_serializers.DocumentDetailSerializer,
    }
    default_serializer_class = documets_serializers.DocumentSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = DocumentFilter
    search_fields = ['title']
    filterset_fields = ['type']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)


class HelpApiView(ModelViewSet):
    queryset = Help.objects.all()
    serializer_class = documets_serializers.HelpSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        params = request.GET.get('type', None)
        if params is not None:
            queryset = queryset.filter(type=params)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = documets_serializers.DocumentTypeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)