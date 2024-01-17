import logging

from elasticsearch_dsl import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttpublicApi.permissions import IsPublicApiAuthorized

from rttlimitManagement.services.limit_core_service import LimitCoreService
from rttlimitManagement.services.exemption_existence_check import ExemptionExistenceCheck
from rttregulation.documents import RegulatoryFrameworkDocument
from rttsubstance.documents import SubstanceDocument
from rttregulation.services.regulation_tagged_region_service import RegulationTaggedRegionService

logger = logging.getLogger(__name__)


class RegulationLimitPublicApi(APIView):
    permission_classes = [IsPublicApiAuthorized]

    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-717
        """
        try:
            regulatory_framework_id = request.data.get('regulatory_framework_id', None)
            regulation_id = request.data.get('regulation_id', None)
            substance_id = request.data.get('substance_id', None)
            product_category_id = request.data.get('product_category_id', None)
            material_category_id = request.data.get('material_category_id', None)
            explode_family = request.data.get('explode_family', 'true').lower()

            filters = {
                'regulatory_frameworks': [regulatory_framework_id] if regulatory_framework_id else None,
                'regulations': [regulation_id] if regulation_id else None,
                'substances': [substance_id] if substance_id else None,
                'product_categories': [product_category_id] if product_category_id else None,
                'material_categories': [material_category_id] if material_category_id else None,
                'from_date': request.data.get('from_date', None)
            }
            limit = int(request.data.get('limit', 10))
            skip = int(request.data.get('skip', 0))
            organization_id = request.public_api.get('organization_id', None)
            result_list = []
            exclude_deleted: bool = True
            if filters['from_date']:
                exclude_deleted = False
            regulation_substance_limit_qs = LimitCoreService().get_regulation_substance_limit_queryset(organization_id,
                                                                                                       filters,
                                                                                                       exclude_deleted=exclude_deleted)
            regulation_substance_limit_qs = regulation_substance_limit_qs[skip:limit + skip]
            for reg_substance_limit in regulation_substance_limit_qs:
                has_exemptions = False
                # An object with the regulatory framework, if the limit is associated with a framework
                framework_obj = {}
                if reg_substance_limit.regulatory_framework:
                    has_exemptions = ExemptionExistenceCheck().has_exemption_data(
                        reg_substance_limit.regulatory_framework.id, is_regulation=False,
                        substance_id=reg_substance_limit.substance.id)
                    region_list = []
                    for region in reg_substance_limit.regulatory_framework.regions:
                        region_list.append({
                            'id': region.id,
                            'name': region.name
                        })
                    framework_obj = {
                        'id': reg_substance_limit.regulatory_framework.id,
                        'name': reg_substance_limit.regulatory_framework.name,
                        'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                            organization_id, reg_substance_limit.regulatory_framework.product_categories,
                            serialize=True),
                        'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                            organization_id, reg_substance_limit.regulatory_framework.material_categories,
                            serialize=True),
                        'regions': region_list
                    }
                # An object with the regulation, if the limit is associated with a regulation
                regulation_obj = {}
                if reg_substance_limit.regulation:
                    has_exemptions = ExemptionExistenceCheck().has_exemption_data(
                        reg_substance_limit.regulation.id, is_regulation=True,
                        substance_id=reg_substance_limit.substance.id)
                    region_list = []
                    if reg_substance_limit.regulation.regulatory_framework:
                        region_list = RegulationTaggedRegionService().get_region_data(
                            framework_id=reg_substance_limit.regulation.regulatory_framework.id)
                    regulation_obj = {
                        'id': reg_substance_limit.regulation.id,
                        'name': reg_substance_limit.regulation.name,
                        'product_categories': CategoryValidatorServices().get_relevant_product_categories(
                            organization_id, reg_substance_limit.regulation.product_categories, serialize=True),
                        'material_categories': CategoryValidatorServices().get_relevant_material_categories(
                            organization_id, reg_substance_limit.regulation.material_categories, serialize=True),
                        'regions': region_list
                    }
                limit_data = {
                    'regulatory_framework': framework_obj,
                    'regulation': regulation_obj,
                    # object representing the substance
                    'substance': {
                        'id': reg_substance_limit.substance.id,
                        'name': reg_substance_limit.substance.name,
                        'es': reg_substance_limit.substance.ec_no,
                        'cas': reg_substance_limit.substance.cas_no,
                        'is_family': reg_substance_limit.substance.is_family,
                        'explode_family': None
                    },
                    'last_update': reg_substance_limit.modified,
                    'date_in_force': reg_substance_limit.date_into_force,
                    'has_exemptions': has_exemptions,
                    'limit_scope': reg_substance_limit.scope,
                    'limit_value': reg_substance_limit.limit_value,
                    'limit_uom': reg_substance_limit.measurement_limit_unit,
                    'limit_note': reg_substance_limit.limit_note,
                    'limit_status': reg_substance_limit.status
                }
                result_list.append(limit_data)
                if explode_family == 'true' and reg_substance_limit.substance.is_family:
                    child_substances = SubstanceDocument.search().filter(
                        'nested',
                        path='substance_family',
                        query=Q('match', substance_family__family__id=reg_substance_limit.substance.id)
                    )
                    for substance in child_substances:
                        child_substance_limit_data = limit_data.copy()
                        child_substance_limit_data['substance'] = {
                            'id': substance.id,
                            'name': substance.name,
                            'es': substance.ec_no,
                            'cas': substance.cas_no,
                            'is_family': substance.is_family,
                            'explode_family': reg_substance_limit.substance.name
                        }
                        result_list.append(child_substance_limit_data)

            response = {
                'count': regulation_substance_limit_qs.count(),
                'results': result_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
