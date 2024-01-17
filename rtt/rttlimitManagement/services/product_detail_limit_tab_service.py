from elasticsearch_dsl import Q

from rttlimitManagement.services.exemption_existence_check import ExemptionExistenceCheck
from rttlimitManagement.services.additional_attributes_data_service import AdditionalAttributesDataService
from rttregulation.services.regulation_tagged_region_service import RegulationTaggedRegionService
from rttsubstance.services.relevant_substance_service import SubstanceCoreService
from rttcore.services.system_filter_service import SystemFilterService


class LimitInProductDetailsService:
    # This service is for prepare Limit list in product details page to an organization and apply filter.
    @staticmethod
    def get_regulation_limit_object(regulation_substance_limit, regulation, is_regulation):
        region_list = []
        if not is_regulation:
            for region in regulation.regions:
                region_list.append({
                    'id': region.id,
                    'name': region.name
                })
        if is_regulation and regulation.regulatory_framework:
            region_list = RegulationTaggedRegionService().get_region_data(
                framework_id=regulation.regulatory_framework.id)
        is_substance_relevant = True
        has_exemption = ExemptionExistenceCheck().has_exemption_data(
            regulation.id, is_regulation, substance_id=regulation_substance_limit.substance.id)
        result = {
            'id': regulation_substance_limit.id,
            'regulation': {
                'id': regulation.id,
                'name': regulation.name,
                'is_regulation': is_regulation,
            },
            'has_exemption': has_exemption,
            'substance': {
                'id': regulation_substance_limit.substance.id,
                'name': regulation_substance_limit.substance.name,
                'cas_no': regulation_substance_limit.substance.cas_no,
                'ec_no': regulation_substance_limit.substance.ec_no,
                'is_relevant': is_substance_relevant
            },
            'regions': region_list,
            'scope': regulation_substance_limit.scope,
            'limit': regulation_substance_limit.limit_value,
            'limit_unit': regulation_substance_limit.measurement_limit_unit,
            'limit_note': regulation_substance_limit.limit_note,
            'additional_attributes': AdditionalAttributesDataService().get_additional_attributes_data(
                regulation_substance_limit.id, regulation.id, is_regulation)
        }
        return result

    @staticmethod
    def get_filtered_limit_queryset(regulation_substance_limit_qs, search_keyword):
        search_keyword = search_keyword.lower()
        regulation_substance_limit_qs = regulation_substance_limit_qs.query(
            # any keyword. which will be searched in substance name
            Q('match', substance__name='*{}*'.format(search_keyword)) |
            # any keyword. which will be searched in substance CAS
            Q('match', substance__cas_no=search_keyword) |
            # any keyword. which will be searched in substance ES
            Q('match', substance__ec_no=search_keyword) |
            # any keyword. which will be searched in scope
            Q('match', scope=search_keyword) |
            # any keyword. which will be searched in framework name
            Q('match', regulatory_framework__name=search_keyword) |
            # # any keyword. which will be searched in regulation name
            Q('match', regulation__name=search_keyword)
        ).sort("_score")

        return regulation_substance_limit_qs

    @staticmethod
    def get_product_related_framework_id_list(organization_id, product_category_id_list, material_category_id_list,
                                              regions):
        results = []
        # apply system filter
        framework_doc_qs = SystemFilterService().get_system_filtered_regulatory_framework_queryset(organization_id)
        # filter by regions
        if regions:
            framework_doc_qs = framework_doc_qs.filter(
                Q('nested',
                  path='regions',
                  query=Q('terms', regions__id=regions))
            )
        # filter by product cat and material cat
        framework_doc_qs = framework_doc_qs.filter(
            Q('nested',
              path='product_categories',
              query=Q('terms', product_categories__id=product_category_id_list)) |
            Q('nested',
              path='material_categories',
              query=Q('terms', material_categories__id=material_category_id_list))
        ).source(['id'])
        # take all values
        framework_doc_qs = framework_doc_qs[0: framework_doc_qs.count()]
        # store the ids and return
        for framework in framework_doc_qs:
            results.append(framework.id)
        return results

    @staticmethod
    def get_product_related_regulation_id_list(organization_id, product_category_id_list, material_category_id_list,
                                               regions):
        results = []
        # apply system filter
        regulation_doc_qs = SystemFilterService().get_system_filtered_regulation_document_queryset(organization_id)
        # filter by regions
        if regions:
            regulation_doc_qs = regulation_doc_qs.filter(
                Q('nested',
                  path='regulatory_framework.regions',
                  query=Q('terms', regulatory_framework__regions__id=regions))
            )
        # filter by product_cat and material_cat
        regulation_doc_qs = regulation_doc_qs.filter(
            Q('nested',
              path='product_categories',
              query=Q('terms', product_categories__id=product_category_id_list)) |
            Q('nested',
              path='material_categories',
              query=Q('terms', material_categories__id=material_category_id_list))
        ).source(['id'])
        # take all the value
        regulation_doc_qs = regulation_doc_qs[0: regulation_doc_qs.count()]
        # store the ids and return
        for regulation in regulation_doc_qs:
            results.append(regulation.id)
        return results

    @staticmethod
    def get_product_related_substance_id_list(organization_id, product_id, regions, product_detail_page=False):
        results = []
        # filter for SubstanceCoreService
        filters = {
            'products': [product_id],
            'regions': regions if regions else None,
        }
        # apply SubstanceCoreService filter
        substance_doc_qs = SubstanceCoreService.get_filtered_substance_queryset(
            organization_id, filters, product_detail_page=product_detail_page).source(['id'])
        # take all the dos_qs --> pagination
        substance_doc_qs = substance_doc_qs[0:substance_doc_qs.count()]
        # store the ids in a list and return
        for substance in substance_doc_qs:
            results.append(substance.id)
        return results
