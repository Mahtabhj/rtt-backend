import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from elasticsearch_dsl import Q

from rttpublicApi.permissions import IsPublicApiAuthorized
from rttsubstance.models import Substance, SubstancePropertyDataPoint, Property
from rttsubstance.documents import SubstanceDocument

logger = logging.getLogger(__name__)


class SubstancePublicApi(APIView):
    permission_classes = [IsPublicApiAuthorized]

    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-718
        """
        try:
            organization_id = request.public_api.get('organization_id', None)
            substance_ids = request.data.get('ids', [])
            from_date = request.data.get('from_date', None)
            family_id = request.data.get('family_id', None)
            limit = int(request.data.get('limit', 10))
            skip = int(request.data.get('skip', 0))

            if family_id:
                # if family_id is provided, return all substances of this family
                substance_id_list = self.get_family_substance_id_list(int(family_id))
                substance_doc_qs: SubstanceDocument = SubstanceDocument().search().filter(
                    'terms', id=substance_id_list
                )
            else:
                # list of all substances in the account(organization)
                substance_doc_qs: SubstanceDocument = SubstanceDocument.search().filter(
                    'nested',
                    path='uses_and_application_substances',
                    query=Q('match', uses_and_application_substances__organization__id=organization_id)
                )
            if substance_ids:
                substance_ids = substance_ids.split(',')
                substance_doc_qs = substance_doc_qs.filter('terms', id=substance_ids)

            if from_date:
                # If the "from date" is provided, the API will return all substances with properties that were added or
                # updated on or after the "from_date"
                # TODO: need to do query by PropertyDataPoint model
                substance_ids_list = list(Substance.objects.filter(
                    substance_property_data_point_relation__property_data_point__modified__gte=from_date).values_list(
                    'id', flat=True))
                substance_doc_qs = substance_doc_qs.filter(
                    Q('range', modified={'gte': from_date}) |
                    Q('terms', id=substance_ids_list)
                )
            count = substance_doc_qs.count()
            substance_doc_qs = substance_doc_qs[skip:limit + skip]

            results = []
            for substance in substance_doc_qs:
                property_list = self.get_property_list(substance.id, organization_id)

                families_list = []
                for sub_family in substance.substance_family:
                    families_list.append({
                        'id': sub_family.family.id,
                        'name': sub_family.family.name,
                        'family_added_on': sub_family.modified,
                        'family_source': sub_family.family_source
                    })
                results.append({
                    'id': substance.id,
                    'name': substance.name,
                    'cas_no': substance.cas_no,
                    'ec_no': substance.ec_no,
                    'last_update': substance.modified,
                    'property_list': property_list,
                    'use_and_application': [{'id': use_and_app.id, 'name': use_and_app.name}
                                            for use_and_app in substance.uses_and_application_substances if
                                            use_and_app.organization.id == organization_id],
                    'families': families_list
                })
            response_data = {
                'count': count,
                'results': results
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_family_substance_id_list(family_id):
        child_substance_id_list = []
        is_family = Substance.objects.filter(is_family=True, id=family_id).exists()
        if is_family:
            child_substance_id_list = list(
                Substance.objects.filter(substance_family__family=family_id).values_list(
                    'id', flat=True))

        return child_substance_id_list

    @staticmethod
    def get_property_list(substance_id, organization_id):
        property_list = []
        properties = Property.objects.filter(
            prioritization_strategy_properties__organization_id=organization_id,
            property_data_property__substance_property_data_point_property_data_point__substance_id=substance_id
        ).distinct().order_by('id')
        for property_data in properties:
            data = {
                'id': property_data.id,
                'name': property_data.name,
                'property_data_point': []
            }
            substance_property_data_points = SubstancePropertyDataPoint.objects.filter(
                property_data_point__property__id=property_data.id,
                substance_id=substance_id).select_related('property_data_point')
            for data_point in substance_property_data_points:
                data['property_data_point'].append({
                    'data_point_id': data_point.property_data_point.id,
                    'data_point_name': data_point.property_data_point.name,
                    'data_point_value': data_point.value,
                    'data_point_updated_on': data_point.property_data_point.modified
                })
            property_list.append(data)

        return property_list
