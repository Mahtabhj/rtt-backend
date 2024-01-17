from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import requests
from hashlib import sha256
from datetime import datetime
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import logging
import copy
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Prefetch

from rttcore.permissions import IsSuperUserOrStaff
from rttsubstance.filters import SubstancePropertyDataPointFilter
from rttsubstance.models import SubstancePropertyDataPoint, Property, PropertyDataPoint
from rttsubstance.serializers import SubstancePropertyDataPointListSerializer, SubstancePropertyDataPointSerializer, \
    SubstancePropertyDataPointUpdateSerializer

logger = logging.getLogger(__name__)


class AdminSubstanceDataViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)
    queryset = SubstancePropertyDataPoint.objects.all()
    serializer_classes = {
        'list': SubstancePropertyDataPointListSerializer,
        'retrieve': SubstancePropertyDataPointListSerializer,
        'update': SubstancePropertyDataPointUpdateSerializer,
        'partial_update': SubstancePropertyDataPointUpdateSerializer,
        'create': SubstancePropertyDataPointSerializer,
        'get_substance_data_edit_options': SubstancePropertyDataPointListSerializer,
    }
    default_serializer_class = SubstancePropertyDataPointSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'patch', 'head']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = SubstancePropertyDataPointFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        queryset = self.queryset

        # Any keyword which will be searched in substance_name, substance_cas_no, substance_ec_no
        substance = self.request.GET.get('substance', None)
        if substance:
            queryset = queryset.filter(
                Q(substance__name__icontains=substance) | Q(substance__ec_no__icontains=substance) |
                Q(substance__cas_no__icontains=substance))

        return queryset

    def list(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1160
        """
        try:
            limit = int(request.GET.get('limit', 100))
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
        doc: https://chemycal.atlassian.net/browse/RTT-1161
        """
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                substance_data_obj = serializer.save()
                if request.data.get('image_url', None):
                    image_path = self.get_image_object_from_url(request.data['image_url'])
                    substance_data_obj.image = image_path
                    substance_data_obj.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1162
        """
        try:
            instance = self.get_object()
            data = copy.deepcopy(request.data)
            if not request.data.get('modified', None):
                data['modified'] = timezone.now()
            serializer = self.get_serializer(instance, data=data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='delete')
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'substance_data': openapi.Schema(type=openapi.TYPE_ARRAY,
                                             description='List of substance_property_data_point ID',
                                             items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'date': openapi.Schema(type=openapi.TYPE_STRING,
                                   description='date to be saved in the selected records'),
        }
    ))
    def substance_data(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1163
        """
        try:
            substance_data = request.data.get('substance_data', None)
            date = request.data.get('date', timezone.now())
            if not substance_data:
                return Response({"message": "substance_data must be sent"}, status=status.HTTP_400_BAD_REQUEST)
            successful_operation_count = 0
            for substance_data_id in substance_data:
                try:
                    substance_data_obj = SubstancePropertyDataPoint.objects.get(id=substance_data_id)
                    substance_data_obj.status = 'deleted'
                    substance_data_obj.modified = date
                    substance_data_obj.save()
                    successful_operation_count += 1
                except Exception as exc:
                    logger.error(str(exc), exc_info=True)
            response = {
                'message': f"{successful_operation_count} substance_data(s) have been deleted"
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='filtered-substance-data-list')
    def filtered_substance_data_list(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1160
        When the “select all” radio button will be clicked, add a button that will allow the user to select all records
        of the DB. Display this button only if a filter is applied to the table
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

    @staticmethod
    @action(detail=False, methods=['get'], url_path='property-options')
    def properties_options(request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1161
        """
        try:
            response = []
            property_queryset = Property.objects.prefetch_related('property_data_property')
            for property_data in property_queryset:
                property_obj = {
                    'id': property_data.id,
                    'name': property_data.name,
                    'property_data_points': [{'id': property_data_point.id, 'name': property_data_point.name} for
                                             property_data_point in property_data.property_data_property.all()]
                }
                response.append(property_obj)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='property-data-point-options')
    def get_substance_data_edit_options(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1162
        """
        try:
            if not request.data.get('property', None) or not request.data.get('substance'):
                return Response({"message": "property ID AND Substance ID must be sent"},
                                status=status.HTTP_400_BAD_REQUEST)
            property_id = request.data['property']
            substance_id = request.data['substance']
            property_data_point_qs = PropertyDataPoint.objects.filter(property_id=property_id).prefetch_related(
                Prefetch('substance_property_data_point_property_data_point',
                         queryset=SubstancePropertyDataPoint.objects.filter(substance_id=substance_id))).order_by(
                'substance_property_data_point_property_data_point__id')
            response = []
            visited_property_data_point = {}
            for property_data_point in property_data_point_qs:
                if str(property_data_point.id) not in visited_property_data_point:
                    visited_property_data_point[str(property_data_point.id)] = True
                    if len(property_data_point.substance_property_data_point_property_data_point.all()) > 0:
                        for substance_property_data_point in \
                                property_data_point.substance_property_data_point_property_data_point.all():
                            substance_property_data_point_obj = {
                                'id': substance_property_data_point.id,
                                'substance': substance_property_data_point.substance.id,
                                'property_data_point': substance_property_data_point.property_data_point.id,
                                'value': substance_property_data_point.value,
                                'image': substance_property_data_point.image.url if substance_property_data_point.image
                                else None,
                                'status': substance_property_data_point.status,
                                'modified': substance_property_data_point.modified,
                            }
                            property_data_point_obj = {
                                'id': property_data_point.id,
                                'name': property_data_point.name,
                                'substance_property_data_point': substance_property_data_point_obj
                            }
                            response.append(property_data_point_obj)
                    else:
                        property_data_point_obj = {
                            'id': property_data_point.id,
                            'name': property_data_point.name,
                            'substance_property_data_point': None,
                        }
                        response.append(property_data_point_obj)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_image_object_from_url(image_url):
        try:
            response = requests.get(image_url, allow_redirects=False)
            seed_str = response.url + str(datetime.now())
            unique_name = sha256(seed_str.encode()).hexdigest()
            unique_name = unique_name[:20]
            image_path = f'media/substance_property_data_point/{unique_name}.png'
            image = default_storage.save(image_path, ContentFile(response.content))
            return image
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return None
