from elasticsearch_dsl import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from rttcore.services.dashboard_services import DashboardService
from rttproduct.documents import ProductDocument, ProductCategoryDocument, MaterialCategoryDocument
from rttproduct.serializers.serializers import ProductCategoryIdNameSerializer, MaterialCategoryIdNameSerializer
from rttproduct.services.category_validator_services import CategoryValidatorServices
from rttproduct.services.product_services import ProductServices
from rttregulation.documents import RegulationDocument, RegulatoryFrameworkDocument
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttcore.services.id_search_service import IdSearchService


class DashboardKeyFiguresApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            product_category = request.data.get('product_categories', None)
            material_category = request.data.get('material_categories', None)
            regions = request.data.get('regions', None)
            topics = request.data.get('topics', None)
            related_products = request.data.get('related_products', None)
            related_regulations = request.data.get('related_regulations', None)
            related_frameworks = request.data.get('related_frameworks', None)
            from_date = request.data.get('from_date', None)
            to_date = request.data.get('to_date', None)
            news = request.data.get('news', None)
            regulations = request.data.get('regulations', None)
            frameworks = request.data.get('frameworks', None)

            filters = {
                'topics': topics,
                'regions': regions,
                'product_categories': product_category,
                'material_categories': material_category,
                'from_date': from_date,
                'to_date': to_date,
                'news': news,
                'regulations': regulations,
                'frameworks': frameworks,
                'related_products': related_products,
                'related_regulations': related_regulations,
                'related_frameworks': related_frameworks,
            }

            organization_id = request.user.organization_id

            response = {
                'products': {
                    'length': 0,  # queryset.count() if queryset else 0
                    'filtered_items_length': 0,  # len(product_category) if product_category else 0
                    'categories': {
                        'product_categories': {'title': 'Product categories', 'options': []},
                        'related_products': {'title': 'Related products', 'options': []}
                    }
                },
                'material': {
                    'length': 0,  # len(material_category) if material_category else 0
                    'categories': {
                        'material_categories': {'title': 'Material categories', 'options': []}
                    }
                },
                'regulations': {
                    'length': 0,  # regulation_queryset.count() if regulation_queryset else 0
                    'filtered_items_length': 0,  # len(regulation) if regulation else 0
                    'categories': {
                        # 'regions': {'title': 'Regions', 'options': []},
                        'related_frameworks': {'title': 'Related frameworks', 'options': []},
                        'related_regulations': {'title': 'Related regulations', 'options': []}
                    },
                }
            }
            if topics or regions or product_category or material_category or related_products or related_regulations \
                    or related_frameworks or (from_date and to_date) or news or regulations or frameworks:

                dashboard_service = DashboardService()

                # product_queryset = dashboard_service.get_filtered_product_queryset(filters, ProductDocument.search()
                #                                                                    .filter('match',
                #                                                                            organization__id=organization_id))
                news_queryset = []
                framework_queryset = []
                regulation_queryset = []

                if dashboard_service.is_return_data(filters, 'news'):
                    news_queryset = dashboard_service.get_filtered_news_queryset(filters, organization_id)
                    news_queryset = news_queryset[0:news_queryset.count()]

                if dashboard_service.is_return_data(filters, 'regulations'):
                    regulation_queryset = dashboard_service.get_filtered_regulation_queryset(filters, organization_id)
                    regulation_queryset = regulation_queryset[0:regulation_queryset.count()]

                if dashboard_service.is_return_data(filters, 'frameworks'):
                    framework_queryset = dashboard_service.get_filtered_regulatory_framework_queryset(filters,
                                                                                                      organization_id)
                    framework_queryset = framework_queryset[0:framework_queryset.count()]

                response, news_related_reg_len, news_related_fw_len = self.get_filtered_options(
                    response, filters, organization_id, news_queryset, regulation_queryset, framework_queryset)
                response['regulations']['length'] = (regulation_queryset.count() if regulation_queryset else 0) + (
                    framework_queryset.count() if framework_queryset else 0) + news_related_reg_len + news_related_fw_len
            else:
                product_queryset = ProductDocument.search().filter('match', organization__id=organization_id)
                regulation_queryset = RegulationDocument.search().filter(Q('match', review_status='o'))
                framework_queryset = RegulatoryFrameworkDocument.search().filter(Q('match', review_status='o'))

                product_category_qs = ProductCategoryDocument.search()
                material_category_qs = MaterialCategoryDocument.search()
                # region_qs = RegionDocument.search()s
                response = self.get_all_options(response, product_queryset, regulation_queryset, product_category_qs,
                                                material_category_qs, framework_queryset)
                response['products']['length'] = product_queryset.count()
                response['products']['filtered_items_length'] = product_category_qs.count()
                response['material']['length'] = material_category_qs.count()
                response['regulations']['length'] = regulation_queryset.count() + framework_queryset.count()
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            is_es_rebuild = DashboardService().check_es_exception(ex)
            return self.post(request) if is_es_rebuild \
                else Response({"error": "Server Error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_all_options(response, product_queryset, regulation_queryset, product_category_qs, material_category_qs,
                        framework_queryset):
        for product in product_queryset:
            response['products']['categories']['related_products']['options'].append(
                {'id': product.id, 'name': product.name}
            )
        for regulation in regulation_queryset:
            response['regulations']['categories']['related_regulations']['options'].append(
                {'id': regulation.id, 'name': regulation.name}
            )
        for framework in framework_queryset:
            response['regulations']['categories']['related_frameworks']['options'].append(
                {'id': framework.id, 'name': framework.name}
            )

        response['products']['categories']['product_categories']['options'] = [{'id': data.id, 'name': data.name} for
                                                                               data in product_category_qs]
        response['material']['categories']['material_categories']['options'] = [{'id': data.id, 'name': data.name} for
                                                                                data in material_category_qs]
        # response['regulations']['categories']['regions']['options'] = [{'id': data.id, 'name': data.name} for
        #                                                                data in region_qs]
        return response

    def get_filtered_options(self, response, filters, organization_id,
                             news_queryset, regulation_queryset, framework_queryset):
        product_options = []
        material_options = []
        # region_options = []

        for news in news_queryset:
            product_options.extend(
                CategoryValidatorServices().get_relevant_product_categories(organization_id, news.product_categories,
                                                                            serialize=True))
            material_options.extend(
                CategoryValidatorServices().get_relevant_material_categories(
                    organization_id, news.material_categories, serialize=True, distinct_item=False))

        existing_reg_list = []
        for regulation in regulation_queryset:
            existing_reg_list.append(regulation.id)
            response['regulations']['categories']['related_regulations']['options'].append(
                {'id': regulation.id, 'name': regulation.name}
            )
            product_options.extend(CategoryValidatorServices().get_relevant_product_categories(organization_id,
                                                                                               regulation.product_categories,
                                                                                               serialize=True))
            material_options.extend(CategoryValidatorServices().get_relevant_material_categories(
                organization_id, regulation.material_categories, serialize=True, distinct_item=False))

            # for data in query.regulatory_framework.regions:
            #     region_options.append({'id': data.id, 'name': data.name})

        existing_fw_list = []
        for framework in framework_queryset:
            existing_fw_list.append(framework.id)
            response['regulations']['categories']['related_frameworks']['options'].append(
                {'id': framework.id, 'name': framework.name}
            )
            product_options.extend(CategoryValidatorServices().get_relevant_product_categories(organization_id,
                                                                                               framework.product_categories,
                                                                                               serialize=True))
            material_options.extend(CategoryValidatorServices().get_relevant_material_categories(
                organization_id, framework.material_categories, serialize=True, distinct_item=False))

        news_related_regulation_obj_list, news_related_framework_obj_list = self.get_news_relevant_regulation_id_list(
            organization_id, news_queryset, existing_reg_list, existing_fw_list)
        response['regulations']['categories']['related_regulations']['options'].extend(news_related_regulation_obj_list)
        response['regulations']['categories']['related_frameworks']['options'].extend(news_related_framework_obj_list)


        """
        start finding related_products
        """

        if not filters['product_categories']:
            filters['product_categories'] = []
        filters['product_categories'].extend(list({v['id']: v for v in product_options}))
        filters['product_categories'] = ProductServices().get_all_tree_child_product_category_ids(
            filters['product_categories'])

        if not filters['material_categories']:
            filters['material_categories'] = []
        filters['material_categories'].extend([mat_cat['id'] for mat_cat in material_options])

        if filters['product_categories'] or filters['material_categories']:
            product_queryset = ProductServices().get_related_product_filtered_queryset(
                filters, ProductDocument.search().filter('match', organization__id=organization_id))
            product_queryset = product_queryset[0:product_queryset.count()]
            for query in product_queryset:
                response['products']['categories']['related_products']['options'].append(
                    {'id': query.id, 'name': query.name})
            response['products']['length'] = product_queryset.count()

        """
        end related_products
        """

        response['products']['categories']['product_categories']['options'] = list(
            {v['id']: v for v in product_options}.values())
        response['material']['categories']['material_categories']['options'] = list(
            {v['id']: v for v in material_options}.values())
        # response['regulations']['categories']['regions']['options'] = list(
        #     {v['id']: v for v in region_options}.values())

        response['products']['filtered_items_length'] = len(
            response['products']['categories']['product_categories']['options'])
        response['material']['length'] = len(response['material']['categories']['material_categories']['options'])
        return response, len(news_related_regulation_obj_list), len(news_related_framework_obj_list)

    @staticmethod
    def get_news_relevant_regulation_id_list(organization_id, news_doc_qs, existing_reg_list, existing_fw_list):
        id_search_service = IdSearchService()
        relevant_regulation_service = RelevantRegulationService()
        org_related_reg_list = relevant_regulation_service.get_relevant_regulation_id_organization(organization_id)
        org_related_fw_list = relevant_regulation_service.get_relevant_regulatory_framework_id_organization(organization_id)
        regulation_obj_list = []
        visited_regulation = {}
        framework_obj_list = []
        visited_framework = {}
        for news in news_doc_qs:
            for reg in news.regulations:
                if reg.id in visited_regulation:
                    continue
                if id_search_service.does_id_exit_in_sorted_list(org_related_reg_list, reg.id) and not reg.id in existing_reg_list:
                    regulation_obj_list.append({
                        "id": reg.id,
                        "name": reg.name,
                    })
                visited_regulation[reg.id] = True
            for fw in news.regulatory_frameworks:
                if fw.id in visited_framework:
                    continue
                if id_search_service.does_id_exit_in_sorted_list(org_related_fw_list, fw.id) and not fw.id in existing_fw_list:
                    framework_obj_list.append({
                        "id": fw.id,
                        "name": fw.name,
                    })
                visited_framework[fw.id] = True
        return regulation_obj_list, framework_obj_list
