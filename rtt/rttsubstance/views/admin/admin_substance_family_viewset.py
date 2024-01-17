import copy
import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.decorators import action

from rttcore.permissions import IsSuperUserOrStaff
from rttsubstance.filters import SubstanceFamilyFilter
from rttsubstance.models import Substance, SubstanceFamily
from rttsubstance.serializers import SubstanceFamilySerializer, SubstanceFamilyUpdateSerializer, SubstanceSerializer

logger = logging.getLogger(__name__)


class AdminSubstanceFamilyViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsSuperUserOrStaff,)
    queryset = Substance.objects.filter(is_family=True)
    serializer_classes = {
        'list': SubstanceFamilySerializer,
        'retrieve': SubstanceFamilySerializer,
        'update': SubstanceFamilyUpdateSerializer,
        'partial_update': SubstanceFamilyUpdateSerializer,
        'create': SubstanceFamilySerializer,
    }
    default_serializer_class = SubstanceSerializer
    lookup_field = 'id'
    http_method_names = ['get', 'post', 'put', 'patch', 'head']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filter_class = SubstanceFamilyFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def list(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1205
        """
        try:
            limit = int(request.GET.get('limit', 20))
            skip = int(request.GET.get('skip', 0))
            queryset = self.filter_queryset(self.queryset)
            count = queryset.count()
            substance_queryset = queryset[skip:skip + limit]

            serializer = self.get_serializer(substance_queryset, many=True)
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
        doc: https://chemycal.atlassian.net/browse/RTT-1206
        """
        try:
            if request.data.get('name', None):
                is_exists_substance = Substance.objects.filter(name__exact=request.data['name']).exists()
                if is_exists_substance:
                    return Response({"error": "That family already exist"}, status=status.HTTP_400_BAD_REQUEST)
            if request.data.get('chemycal_id', None):
                is_exists_substance = Substance.objects.filter(chemycal_id__exact=request.data['chemycal_id']).exists()
                if is_exists_substance:
                    return Response({"error": "That family already exist"}, status=status.HTTP_400_BAD_REQUEST)
            data = copy.deepcopy(request.data)
            data['is_family'] = True
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='delete')
    def delete_substance_family(self, request, id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1207
        """
        try:
            substance_exist = SubstanceFamily.objects.filter(family_id=id).exists()
            if substance_exist:
                return Response({"message": "The selected Family contains Substances!"},
                                status=status.HTTP_400_BAD_REQUEST)
            substance = Substance.objects.filter(pk=id).first()
            substance.is_family = False
            substance.save()
            response = {
                'message': f"The substance family has been deleted successfully."
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'], url_path='remove-substance-from-family')
    def remove_substance_from_the_family(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1208
        """
        try:
            family_id = request.data.get('family_id', None)
            substance_ids = request.data.get('substance_id', None)
            SubstanceFamily.objects.filter(Q(family_id=family_id) & Q(substance_id__in=substance_ids)).delete()
            response = {
                'message': f"The substances has been removed successfully from family."
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1208
        {Change the Chemycal id field, Change the Name filed (family name)}
        """
        try:
            instance = self.get_object()
            if request.data.get('name', None):
                is_exists_substance = Substance.objects.filter(Q(name__exact=request.data['name']) &
                                                               ~Q(id=instance.id)).exists()
                if is_exists_substance:
                    return Response({"error": "That family already exist"}, status=status.HTTP_400_BAD_REQUEST)
            if request.data.get('chemycal_id', None):
                is_exists_substance = Substance.objects.filter(Q(chemycal_id__exact=request.data['chemycal_id']) &
                                                               ~Q(id=instance.id)).exists()
                if is_exists_substance:
                    return Response({"error": "That family already exist"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='tagged-substances')
    def tagged_substance_list(self, request, id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1208
        """
        try:
            limit = request.data.get('limit', 100)
            skip = request.data.get('skip', 0)
            filters = {
                'substance': request.data.get('substance', None),
                'cas_no': request.data.get('cas_no', None),
                'ec_no': request.data.get('ec_no', None)
            }
            substance_queryset = Substance.objects.filter(substance_family__family_id=id)
            substance_queryset = self.apply_substance_family_edit_page_filter(substance_queryset, filters)
            result_count = substance_queryset.count()
            substance_queryset = substance_queryset[skip:skip + limit]

            substance_list = []
            for substance in substance_queryset:
                substance_list.append({
                    'id': substance.id,
                    'name': substance.name,
                    'ec_no': substance.ec_no,
                    'cas_no': substance.cas_no
                })
            response = {
                'count': result_count,
                'results': substance_list,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='all-tagged-substances-id')
    def all_tagged_substance_list(self, request, id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1208
        """
        try:
            filters = {
                'substance': request.data.get('substance', None),
                'cas_no': request.data.get('cas_no', None),
                'ec_no': request.data.get('ec_no', None)
            }
            substance_queryset = Substance.objects.filter(substance_family__family_id=id)
            substance_queryset = self.apply_substance_family_edit_page_filter(substance_queryset, filters)

            substance_list = list(substance_queryset.values_list('id', flat=True))
            return Response(substance_list, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def apply_substance_family_edit_page_filter(queryset, filters=None):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1201
        :param substance-queryset queryset: required. django-queryset
        :param dict filters: optional. Additional filter options. Sample filters dict:
                        filters = {
                           'substance': string or None,
                           'cas_no': string or None,
                           'ec_no': string or None,
                        }
        """
        # if no filter is given return the queryset
        if not filters:
            return queryset

        # filter by substance name
        if filters.get('substance', None):
            queryset = queryset.filter(name__icontains=filters['substance'])

        # filter by substance cas_no
        if filters.get('cas_no', None):
            queryset = queryset.filter(cas_no__icontains=filters['cas_no'])

        # filter by substance ec_no
        if filters.get('ec_no', None):
            queryset = queryset.filter(ec_no__icontains=filters['ec_no'])

        return queryset

    @action(detail=True, methods=['post'], url_path='add-or-remove-substance')
    def add_or_remove_substance_in_substance_family(self, request, id):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-1210 --> remove
        doc: https://chemycal.atlassian.net/browse/RTT-1209 --> manual add
        """
        try:
            action_name = request.data.get('action', None)
            if action_name not in ['add', 'remove']:
                return Response({"message": "add or remove will be sent in action payload"},
                                status=status.HTTP_400_BAD_REQUEST)
            substances_id_list = request.data.get('substances', None)
            if not substances_id_list:
                return Response({"message": "substances must be sent"}, status=status.HTTP_400_BAD_REQUEST)

            if action_name.lower() == 'add':
                for substance_id in substances_id_list:
                    try:
                        SubstanceFamily.objects.create(family_id=id, substance_id=substance_id)
                    except Exception as exc:
                        logger.error(str(exc), exc_info=True)
            else:
                SubstanceFamily.objects.filter(family_id=id, substance_id__in=substances_id_list).delete()
            return Response({"message": f"{action_name} succeed"}, status=status.HTTP_200_OK)

        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
