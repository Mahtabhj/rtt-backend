import logging
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action

from rttcore.permissions import IsActiveSubstanceModule
from rttsubstance.models import Property, SubstanceUsesAndApplication, Substance, PrioritizationStrategy
from rttsubstance.serializers import PropertySerializer, SubstanceUsesAndApplicationSerializer, \
    SubstanceUsesAndApplicationUpdateSerializer

logger = logging.getLogger(__name__)


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsActiveSubstanceModule]

    def get_queryset(self):
        return self.queryset.filter(
            prioritization_strategy_properties__organization_id=self.request.user.organization_id).distinct()

    @action(detail=False, methods=['GET'], url_path='prioritization-strategy-tagged-properties')
    def get_prioritization_strategy_tagged_properties(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if request.GET.get("prioritization_strategy_id", None):
                default_org_strategy_id = request.GET["prioritization_strategy_id"]
            else:
                default_org_strategy = PrioritizationStrategy.objects.filter(
                    organization_id=request.user.organization_id, default_org_strategy=True).first()
                default_org_strategy_id = default_org_strategy.id
            queryset = queryset.filter(
                prioritization_strategy_properties__id=default_org_strategy_id,
                property_data_property__substance_property_data_point_property_data_point__status='active')
            queryset_count = queryset.count()
            results = []
            for property in queryset:
                results.append({
                    "id": property.id,
                    "name": property.name,
                    "short_name": property.short_name,
                    "url_link": property.url_link,
                })
            response = {
                "count": queryset_count,
                "results": results
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "INTERNAL_SERVER_ERROR"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SubstanceUsesAndApplicationViewSet(viewsets.ModelViewSet):
    """
    doc: https://chemycal.atlassian.net/browse/RTT-843
    """
    queryset = SubstanceUsesAndApplication.objects.all()
    serializer_classes = {
        'retrieve': SubstanceUsesAndApplicationSerializer,
        'update': SubstanceUsesAndApplicationUpdateSerializer,
        'partial_update': SubstanceUsesAndApplicationUpdateSerializer,
    }
    default_serializer_class = SubstanceUsesAndApplicationSerializer
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)
    lookup_field = 'id'
    filter_backends = [SearchFilter, ]
    search_fields = ['name']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        organization_id = self.request.user.organization_id
        if organization_id:
            return self.queryset.filter(organization_id=organization_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['organization'] = request.user.organization_id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Invalid ID or don't have the permission to delete"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='substance-count')
    def substance_count(self, request, id=None):
        """
        This function will return number of substances of an Use&app.
        doc:https://chemycal.atlassian.net/browse/RTT-842
        """
        try:
            organization_id = request.user.organization_id
            use_and_app_qs = SubstanceUsesAndApplication.objects.filter(id=id, organization_id=organization_id).exists()
            if not use_and_app_qs:
                return Response({"message": "Invalid UsesAndApplication ID or don't have the permission to delete"},
                                status=status.HTTP_400_BAD_REQUEST)
            substance_count = Substance.objects.filter(uses_and_application_substances__id=id).count()
            return Response({'substance_count': substance_count}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
