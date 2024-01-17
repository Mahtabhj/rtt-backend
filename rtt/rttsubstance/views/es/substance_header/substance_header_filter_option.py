from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from elasticsearch_dsl import Q
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveSubstanceModule
from rttcore.services.system_filter_service import SystemFilterService
from rttproduct.documents import ProductDocument
from rttproduct.serializers.serializers import ProductIdNameSerializer
from rttregulation.documents import RegulationDocument
from rttregulation.serializers.serializers import RegulatoryFrameworkIdNameSerializer
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService


class SubstanceHeaderFilterOptionsResponseSerializer(serializers.Serializer):
    frameworks = RegulatoryFrameworkIdNameSerializer(many=True)
    products = ProductIdNameSerializer(many=True)


class SubstanceHeaderFilterOptions(APIView):
    permission_classes = (IsAuthenticated, IsActiveSubstanceModule)

    '''
    for swagger documentation 
    '''
    user_response = openapi.Response('response', SubstanceHeaderFilterOptionsResponseSerializer)

    @swagger_auto_schema(responses={200: user_response})
    def get(self, request):
        try:
            organization_id = request.user.organization_id
            substance_ids = RelevantSubstanceService().get_organization_relevant_substance_ids(organization_id)
            product_data = []
            regulatory_framework_data = []
            regulation_milestone_tagged_substance_ids = []

            '''
            regulatory_framework filter options
            https://chemycal.atlassian.net/browse/RTT-536
            '''
            regulation_substance_doc_qs = RegulationDocument.search().filter('match', review_status='o').filter(
                Q('nested',
                  path='regulation_milestone.substances',
                  query=Q('terms', regulation_milestone__substances__id=substance_ids))
            ).source(['id'])
            regulation_substance_doc_qs = regulation_substance_doc_qs[0:regulation_substance_doc_qs.count()]
            for regulation_substance in regulation_substance_doc_qs:
                regulation_milestone_tagged_substance_ids.append(regulation_substance.id)

            regulatory_framework_doc_qs = SystemFilterService(). \
                get_system_filtered_regulatory_framework_queryset(organization_id).filter(
                # substance tagged to the framework
                Q('nested',
                  path='substances',
                  query=Q('terms', substances__id=substance_ids)) |
                # substance tagged to milestone of the framework
                Q('nested',
                  path='regulatory_framework_milestone.substances',
                  query=Q('terms', regulatory_framework_milestone__substances__id=substance_ids)) |
                # substance tagged to a regulation linked to the framework
                Q(
                    Q('nested',
                      path='regulation_regulatory_framework',
                      query=Q('match', regulation_regulatory_framework__review_status='o')) &
                    Q('nested',
                      path='regulation_regulatory_framework.substances',
                      query=Q('terms', regulation_regulatory_framework__substances__id=substance_ids))
                ) |
                # substance tagged to milestone of the regulation linked to the framework
                Q('nested',
                  path='regulation_regulatory_framework',
                  query=Q('terms',
                          regulation_regulatory_framework__id=regulation_milestone_tagged_substance_ids))
            ).source(['id', 'name']).sort('name.raw')
            regulatory_framework_doc_qs = regulatory_framework_doc_qs[0:regulatory_framework_doc_qs.count()]
            for regulatory_framework in regulatory_framework_doc_qs:
                regulatory_framework_obj = {
                    'id': regulatory_framework.id,
                    'name': regulatory_framework.name
                }
                regulatory_framework_data.append(regulatory_framework_obj)

            '''
            product filter options
            https://chemycal.atlassian.net/browse/RTT-536
            '''
            product_doc_queryset = ProductDocument.search().filter(
                Q('match', organization__id=organization_id) &
                Q('nested',
                  path='substances',
                  query=Q('terms', substances__id=substance_ids)),
            ).source(['id', 'name']).sort('name')
            product_doc_queryset = product_doc_queryset[0:product_doc_queryset.count()]
            for product in product_doc_queryset:
                product_obj = {
                    'id': product.id,
                    'name': product.name
                }
                product_data.append(product_obj)

            return_data = {
                'frameworks': regulatory_framework_data,
                'products': product_data
            }
            return Response(return_data, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
        return Response({"message": "An Error Occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
