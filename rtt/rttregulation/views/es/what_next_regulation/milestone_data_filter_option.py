from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from elasticsearch_dsl import Q

from rttorganization.services.organization_services import OrganizationService
from rttproduct.documents import MaterialCategoryDocument
from rttregulation.services.what_next_milestone_service import WhatNextMilestoneService
from rttregulation.documents import RegulatoryFrameworkDocument

logger = logging.getLogger(__name__)


class WhatNextMilestoneFilterOption(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'period': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='will filter milestones based on years'),
            'regulatory_frameworks': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of framework ID',
                                                    items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regulations': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of regulation ID',
                                          items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'milestone_types': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of milestone_type ID',
                                              items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'regions': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of region ID',
                                      items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'product_categories': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of product_category ID',
                                                 items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'material_categories': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of material_category ID',
                                                  items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'search': openapi.Schema(type=openapi.TYPE_STRING,
                                     description='Search in milestone name and description'),
            'related_products': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of related_products ID',
                                               items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'status': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of status ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
            'topics': openapi.Schema(type=openapi.TYPE_ARRAY, description='List of topics ID',
                                     items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        }
    ))
    def post(self, request):
        """
        doc: https://chemycal.atlassian.net/browse/RTT-707
        """
        try:
            period = request.data.get('period', None)
            filters = {
                'period_start': period + '-01-01' if period else None,
                'period_end': period + '-12-31' if period else None,
                'regulatory_frameworks': request.data.get('regulatory_frameworks', None),
                'regulations': request.data.get('regulations', None),
                'milestone_types': request.data.get('milestone_types', None),
                'regions': request.data.get('regions', None),
                'product_categories': request.data.get('product_categories', None),
                'material_categories': request.data.get('material_categories', None),
                'related_products': request.data.get('related_products', None),
                'status': request.data.get('status', None),
                'topics': request.data.get('topics', None)
            }
            organization_id = request.user.organization_id
            search_keyword = request.data.get('search', None)
            milestone_doc_queryset = WhatNextMilestoneService().get_what_next_filtered_milestone_document_queryset(
                organization_id, filters, search_keyword)
            milestone_doc_queryset = milestone_doc_queryset[0:milestone_doc_queryset.count()]

            period_list = []
            visited_period = {}
            regulatory_framework_list = []
            visited_regulatory_framework = {}
            regulation_list = []
            visited_regulation = {}
            milestone_type_list = []
            visited_milestone_type = {}
            region_list = []
            visited_region = {}
            product_category_list = []
            visited_product_category = {}
            material_category_list = []
            visited_material_category = {}

            organization_product_category_ids = OrganizationService().get_organization_product_category_ids(
                organization_id)
            organization_material_category_ids = OrganizationService().get_organization_material_category_ids(
                organization_id)

            for milestone in milestone_doc_queryset:
                if milestone.from_date:
                    period = str(milestone.from_date)[:4]  # 'yyyy-mm-dd' of [:4] is 'yyyy'
                    if period not in visited_period:
                        period_list.append({
                            'period': period,
                            'count': 1
                        })
                        visited_period[period] = len(period_list) - 1
                    else:
                        idx = visited_period[period]
                        period_list[idx]['count'] += 1

                if milestone.regulatory_framework:
                    if str(milestone.regulatory_framework.id) not in visited_regulatory_framework:
                        regulatory_framework_list.append({
                            'id': milestone.regulatory_framework.id,
                            'name': milestone.regulatory_framework.name
                        })
                        visited_regulatory_framework[str(milestone.regulatory_framework.id)] = True

                    for region in milestone.regulatory_framework.regions:
                        if str(region.id) not in visited_region:
                            region_list.append({
                                'id': region.id,
                                'name': region.name
                            })
                            visited_region[str(region.id)] = True

                    for product_category in milestone.regulatory_framework.product_categories:
                        if str(product_category.id) not in visited_product_category \
                                and product_category.id in organization_product_category_ids:
                            product_category_list.append({
                                'id': product_category.id,
                                'name': product_category.name
                            })
                            visited_product_category[str(product_category.id)] = True

                    for material_category in milestone.regulatory_framework.material_categories:
                        if str(material_category.id) not in visited_material_category \
                                and material_category.id in organization_material_category_ids:
                            obj = self.get_mat_category_obj(material_category.id)
                            material_category_list.append(obj)
                            visited_material_category[str(material_category.id)] = True

                if milestone.regulation:
                    if str(milestone.regulation.id) not in visited_regulation:
                        regulation_list.append({
                            'id': milestone.regulation.id,
                            'name': milestone.regulation.name
                        })
                        visited_regulation[str(milestone.regulation.id)] = True

                    if milestone.regulation.regulatory_framework:
                        framework_doc_queryset = self.get_region_tagged_framework_queryset(
                            framework_id=milestone.regulation.regulatory_framework.id)
                        for framework in framework_doc_queryset:
                            for region in framework.regions:
                                if str(region.id) not in visited_region:
                                    region_list.append({
                                        'id': region.id,
                                        'name': region.name
                                    })
                                    visited_region[str(region.id)] = True

                    for product_category in milestone.regulation.product_categories:
                        if str(product_category.id) not in visited_product_category \
                                and product_category.id in organization_product_category_ids:
                            product_category_list.append({
                                'id': product_category.id,
                                'name': product_category.name
                            })
                            visited_product_category[str(product_category.id)] = True

                    for material_category in milestone.regulation.material_categories:
                        if str(material_category.id) not in visited_material_category \
                                and material_category.id in organization_material_category_ids:
                            obj = self.get_mat_category_obj(material_category.id)
                            material_category_list.append(obj)
                            visited_material_category[str(material_category.id)] = True

                if milestone.type:
                    if str(milestone.type.id) not in visited_milestone_type:
                        milestone_type_list.append({
                            'id': milestone.type.id,
                            'name': milestone.type.name
                        })
                        visited_milestone_type[str(milestone.type.id)] = True
            response = {
                'period': period_list,
                'regulatory_frameworks': regulatory_framework_list,
                'regulations': regulation_list,
                'milestone_types': milestone_type_list,
                'regions': region_list,
                'product_categories': product_category_list,
                'material_categories': material_category_list
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_region_tagged_framework_queryset(framework_id):
        framework_doc_queryset: RegulatoryFrameworkDocument = RegulatoryFrameworkDocument.search().filter(
            Q('match', id=framework_id)
        ).source(['regions'])
        framework_doc_queryset = framework_doc_queryset[0:framework_doc_queryset.count()]
        return framework_doc_queryset

    @staticmethod
    def get_mat_category_obj(mat_category_id):
        mat_category_doc_qs: MaterialCategoryDocument = MaterialCategoryDocument.search().filter(
            'match', id=mat_category_id).source(['id', 'name', 'industry'])
        result = {}
        for mat_category in mat_category_doc_qs:
            result = {
                'id': mat_category.id,
                'name': mat_category.name,
                'industry': {
                    'id': mat_category.industry.id,
                    'name': mat_category.industry.name
                }
            }
        return result
