from datetime import datetime

import pytz
from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from rttorganization.models.models import Organization, Subscription, SubscriptionType
from rttorganization.serializers import serializers
from rttorganization.services.organization_services import OrganizationService


class OrganizationViewSet(viewsets.ModelViewSet):

    queryset = Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def list(self, request, **kwargs):
        queryset = self.get_queryset().prefetch_related(
            Prefetch('organization_subscriptions',
                     queryset=Subscription.objects.filter(end_date__gte=datetime.now(tz=pytz.UTC))))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(serializers.OrganizationDetailsSerializer(page, many=True).data)
        else:
            serializer = serializers.OrganizationDetailsSerializer(queryset, many=True)
        serialized_data = serializer.data
        for item in serialized_data['results']:
            if len(item['organization_subscriptions']) > 0:
                item['organization_subscriptions'] = item['organization_subscriptions'][0]['type']['name']
            else:
                item['organization_subscriptions'] = 'None'
        return Response(serialized_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def get_relevant_organizations(self, request):
        try:
            '''
            docs: https://chemycal.atlassian.net/browse/RTT-477?focusedCommentId=10849
            '''
            filters = {
                'topics': request.data.get('topics', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'regulations': request.data.get('regulations', None),
                'frameworks': request.data.get('frameworks', None),
            }
            organization_document_queryset = OrganizationService.get_relevant_organizations(filters)
            organization_document_queryset = organization_document_queryset[0: organization_document_queryset.count()]

            response_data = []
            for organization_document in organization_document_queryset:
                organization_data = {
                    'id': organization_document.id,
                    'name': organization_document.name,
                }
                response_data.append(organization_data)
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as ex:
            print(ex)
        return Response({'message': 'An Error Occurred'}, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all().select_related('type', 'organization')
    serializer_class = serializers.SubscriptionSerializer
    permission_class = IsAuthenticated

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        organization_id = self.request.GET.get('organization_id', None)
        if organization_id is not None:
            queryset = queryset.filter(organization_id=int(organization_id))
        serializer = serializers.SubscriptionSerializer(queryset, many=True)
        return Response(serializer.data)


class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionType.objects.all()
    serializer_class = serializers.SubscriptionTypeSerializer
    permission_class = IsAuthenticated
