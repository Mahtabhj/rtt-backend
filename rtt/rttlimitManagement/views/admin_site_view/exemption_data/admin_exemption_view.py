from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from rttcore.permissions import IsSuperUserOrStaff
from rttlimitManagement.models import Exemption

from rttlimitManagement.filters import ExemptionFilter
from rttlimitManagement.serializers import ExemptionDetailSerializer, ExemptionSerializer, ExemptionCreateSerializer, \
    ExemptionUpdateSerializer

logger = logging.getLogger(__name__)


class AdminExemptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)
    queryset = Exemption.objects.all()
    serializer_classes = {
        'list': ExemptionDetailSerializer,
        'retrieve': ExemptionDetailSerializer,
        'create': ExemptionCreateSerializer,
        'update': ExemptionUpdateSerializer,
        'partial_update': ExemptionUpdateSerializer
    }
    default_serializer_class = ExemptionSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'head', 'patch', 'put']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = ExemptionFilter
    search_fields = ['article', 'reference', 'application']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        queryset = self.queryset
        # filter by from_date and to_date on expiration_date, date_into_force, and modified
        from_date = self.request.GET.get('from_date', None)
        to_date = self.request.GET.get('to_date', None)
        if from_date and to_date:
            queryset = queryset.filter(Q(Q(expiration_date__gte=from_date) & Q(expiration_date__lte=to_date)) |
                                       Q(Q(date_into_force__gte=from_date) & Q(date_into_force__lte=to_date)) |
                                       Q(Q(modified__gte=from_date) & Q(modified__lte=to_date)))

        # filter by regions. Any keyword which will be searched in region_name
        region = self.request.GET.get('region', None)
        if region:
            queryset = queryset.filter(Q(regulatory_framework__regions__name__icontains=region) |
                                       Q(regulation__regulatory_framework__regions__name__icontains=region))

        # Any keyword which will be searched in substance_name, substance_cas_no, substance_ec_no
        substance = self.request.GET.get('substance', None)
        if substance:
            queryset = queryset.filter(
                Q(substance__name__icontains=substance) | Q(substance__ec_no__icontains=substance) |
                Q(substance__cas_no__icontains=substance))
        return queryset

    def list(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-930
        """
        try:
            limit = int(request.GET.get('limit', 20))
            skip = int(request.GET.get('skip', 0))
            status_val = request.GET.get('status', None)
            if status_val and status_val not in ['active', 'deleted']:
                return Response({"message": "status value is either 'active' or 'deleted'"},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = self.filter_queryset(self.get_queryset())
            count = queryset.count()
            queryset = queryset[skip:skip + limit]
            serializer = self.get_serializer(queryset, many=True)
            response = {
                'count': count,
                'results': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-931
        """
        try:
            data = request.data.copy()
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-939
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='delete-exemption')
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'exemptions': openapi.Schema(type=openapi.TYPE_ARRAY,
                                         description='List of exemption IDs',
                                         items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'date': openapi.Schema(type=openapi.TYPE_STRING,
                                   description='date to be saved in the selected records'),
        }
    ))
    def delete_exemption(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-939
        """
        try:
            exemptions = request.data.get('exemptions', None)
            date = request.data.get('date', timezone.now())
            if not exemptions:
                return Response({"message": "exemptions must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            successful_operation_count = 0
            for exemption_id in exemptions:
                try:
                    exemption_qs = Exemption.objects.get(id=exemption_id)
                    exemption_qs.status = 'deleted'
                    exemption_qs.modified = date
                    exemption_qs.save()
                    successful_operation_count += 1
                except Exception as exc:
                    logger.error(str(exc), exc_info=True)
            response = {
                'message': f"{successful_operation_count} exemption(s) have been deleted"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='filtered-exemption-list')
    def filtered_exemption_list(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-977
        """
        try:
            status_val = request.GET.get('status', None)
            if status_val and status_val not in ['active', 'deleted']:
                return Response({"message": "status value is either 'active' or 'deleted'"},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = self.filter_queryset(self.get_queryset())
            response = list(queryset.values_list('id', flat=True))
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
