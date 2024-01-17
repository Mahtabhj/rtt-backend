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
from rttlimitManagement.models import RegulationSubstanceLimit, LimitAdditionalAttributeValue
from rttlimitManagement.serializers import RegulationSubstanceLimitSerializer, \
    RegulationSubstanceLimitCreateSerializer, RegulationSubstanceLimitDetailSerializer
from rttlimitManagement.filters import RegulationSubstanceLimitFilter

logger = logging.getLogger(__name__)


class AdminLimitViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)
    queryset = RegulationSubstanceLimit.objects.all()
    serializer_classes = {
        'list': RegulationSubstanceLimitDetailSerializer,
        'retrieve': RegulationSubstanceLimitDetailSerializer,
        'create': RegulationSubstanceLimitCreateSerializer
    }
    default_serializer_class = RegulationSubstanceLimitSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'head']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = RegulationSubstanceLimitFilter
    search_fields = ['scope', 'measurement_limit_unit', 'limit_note']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        queryset = self.queryset
        # received from_date and to_date and apply filter
        from_date = self.request.GET.get('from_date', None)
        to_date = self.request.GET.get('to_date', None)
        if from_date and to_date:
            queryset = queryset.filter(Q(Q(date_into_force__gte=from_date) & Q(date_into_force__lte=to_date)) |
                                       Q(Q(modified__gte=from_date) & Q(modified__lte=to_date)))

        # received max and min vale of limit value and apply filter
        min_limit_value = self.request.GET.get('min_limit_value', None)
        max_limit_value = self.request.GET.get('max_limit_value', None)
        if min_limit_value and max_limit_value:
            queryset = queryset.filter(Q(limit_value__gte=min_limit_value) & Q(limit_value__lte=max_limit_value))

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
        doc: https://chemycal.atlassian.net/browse/RTT-932
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
        doc: https://chemycal.atlassian.net/browse/RTT-933
        """
        try:
            limit_data = {
                'substance': request.data.get('substance', None),
                'regulatory_framework': request.data.get('regulatory_framework', None),
                'regulation': request.data.get('regulation', None),
                'scope': request.data.get('scope', None),
                'limit_value': request.data.get('limit_value', None),
                'measurement_limit_unit': request.data.get('measurement_limit_unit', None),
                'limit_note': request.data.get('limit_note', None),
                'status': request.data.get('status', 'active'),
                'date_into_force': request.data.get('date_into_force', None)
            }
            serializer = self.get_serializer(data=limit_data)
            if serializer.is_valid():
                limit_instance = serializer.save()
                if request.data.get('modified', None):
                    limit_instance.modified = request.data['modified']
                    limit_instance.save(modified=request.data['modified'])
                limit_id = serializer.data.get('id', None)
                additional_attribute_values = request.data.get('additional_attribute_values', None)
                if additional_attribute_values:
                    for additional_att_val in additional_attribute_values:
                        try:
                            LimitAdditionalAttributeValue.objects.create(
                                regulation_substance_limit_id=limit_id,
                                regulation_limit_attribute_id=additional_att_val['attribute_id'],
                                value=additional_att_val['value']
                            )
                        except Exception as exc:
                            logger.error(str(exc), exc_info=True)
                return Response({"message": "created"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='update-limit')
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'limits': openapi.Schema(type=openapi.TYPE_ARRAY,
                                     description='List of limit IDs',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'substance': openapi.Schema(type=openapi.TYPE_NUMBER, description='enter substance_id'),
            'regulatory_framework': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                   description='enter regulatory_framework_id'),
            'regulation': openapi.Schema(type=openapi.TYPE_INTEGER, description='enter regulation_id'),
            'scope': openapi.Schema(type=openapi.TYPE_STRING, description='enter scope'),
            'limit_value': openapi.Schema(type=openapi.TYPE_NUMBER, description='enter limit_value'),
            'measurement_limit_unit': openapi.Schema(type=openapi.TYPE_STRING,
                                                     description='enter measurement_limit_unit'),
            'limit_note': openapi.Schema(type=openapi.TYPE_STRING, description='enter limit_note'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='status, either active/deleted'),
            'date_into_force': openapi.Schema(type=openapi.TYPE_STRING,
                                              description='date_into_force, eg: 2033-01-01T00:00:00.0000Z'),
            'modified': openapi.Schema(type=openapi.TYPE_STRING,
                                       description='modified, eg: 2033-01-01T00:00:00.0000Z'),
            'additional_attribute_values': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                          description='List of limit ID',
                                                          items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                                              'attribute_id': openapi.Schema(
                                                                  type=openapi.TYPE_INTEGER,
                                                                  description='enter attribute_id'),
                                                              'value': openapi.Schema(type=openapi.TYPE_STRING,
                                                                                      description='enter value')})),
            'removed_additional_attributes': openapi.Schema(type=openapi.TYPE_ARRAY,
                                                            description='List of regulation_limit_attribute ID',
                                                            items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        }
    ))
    def update_limit(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-934
        """
        try:
            if not request.data.get('limits', None):
                return Response({"message": "limits ids is required!"},
                                status=status.HTTP_400_BAD_REQUEST)
            limits = request.data.get('limits', None)
            success_operation = 0
            for limit_id in limits:
                try:
                    if request.data.get('regulatory_framework', None) and request.data.get('regulation', None):
                        return Response({"message": "Only regulatory_framework OR regulation can be sent"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    limit_instance = RegulationSubstanceLimit.objects.get(id=limit_id)
                    if len(limits) > 1:
                        # This is bulk update, so need to check which fields are requested to update
                        if 'substance' in request.data:
                            limit_instance.substance_id = request.data['substance']
                        if 'scope' in request.data:
                            limit_instance.scope = request.data['scope']
                        if 'limit_value' in request.data:
                            limit_instance.limit_value = request.data['limit_value']
                        if 'measurement_limit_unit' in request.data:
                            limit_instance.measurement_limit_unit = request.data['measurement_limit_unit']
                        if 'limit_note' in request.data:
                            limit_instance.limit_note = request.data['limit_note']
                        if 'status' in request.data:
                            limit_instance.status = request.data['status']
                        if 'date_into_force' in request.data:
                            limit_instance.date_into_force = request.data['date_into_force']
                        if 'modified' in request.data:
                            limit_instance.save(modified=request.data['modified'])
                        else:
                            limit_instance.save()
                    else:
                        data = {
                            'substance': request.data.get('substance', None),
                            'regulatory_framework': request.data.get('regulatory_framework', None),
                            'regulation': request.data.get('regulation', None),
                            'scope': request.data.get('scope', ''),
                            'limit_value': request.data.get('limit_value', None),
                            'measurement_limit_unit': request.data.get('measurement_limit_unit', ''),
                            'limit_note': request.data.get('limit_note', ''),
                            'status': request.data.get('status', None),
                            'date_into_force': request.data.get('date_into_force', None)
                        }
                        serializer = RegulationSubstanceLimitSerializer(instance=limit_instance, data=data, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            if request.data.get('modified', None):
                                limit_instance.save(modified=request.data['modified'])
                    success_operation += 1
                except Exception as exc:
                    logger.error(str(exc), exc_info=True)
                additional_attribute_values = request.data.get('additional_attribute_values', None)
                if len(limits) == 1 and additional_attribute_values:
                    for additional_att_val in additional_attribute_values:
                        try:
                            LimitAdditionalAttributeValue.objects.update_or_create(
                                regulation_substance_limit_id=limit_id,
                                regulation_limit_attribute_id=additional_att_val['attribute_id'],
                                defaults={'value': additional_att_val['value']}
                            )
                        except Exception as e:
                            logger.error(str(e), exc_info=True)

                # Delete Unchecked limit additional attributes
                if len(limits) == 1 and request.data.get('removed_additional_attributes', None):
                    removed_additional_attributes = request.data['removed_additional_attributes']
                    try:
                        LimitAdditionalAttributeValue.objects.filter(
                            regulation_substance_limit_id=limit_id,
                            regulation_limit_attribute_id__in=removed_additional_attributes,
                        ).delete()
                    except Exception as e:
                        logger.error(str(e), exc_info=True)
            return Response({"message": f"{success_operation} limit(s) have been updated"}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='delete-limit')
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'limits': openapi.Schema(type=openapi.TYPE_ARRAY,
                                     description='List of limit ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'date': openapi.Schema(type=openapi.TYPE_STRING,
                                   description='date to be saved in the selected records'),
        }
    ))
    def delete_limit(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-935
        """
        try:
            limits = request.data.get('limits', None)
            date = request.data.get('date', timezone.now())
            if not limits:
                return Response({"message": "limits must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            successful_operation_count = 0
            for limit_id in limits:
                try:
                    limit_qs = RegulationSubstanceLimit.objects.get(id=limit_id)
                    limit_qs.status = 'deleted'
                    limit_qs.modified = date
                    limit_qs.save(modified=date)
                    successful_operation_count += 1
                except Exception as exc:
                    logger.error(str(exc), exc_info=True)
            response = {
                'message': f"{successful_operation_count} limit(s) have been deleted"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='filtered-limit-list')
    def filtered_limit_list(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-976
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
