import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rttcore.permissions import IsActiveDocumentManagementModule
from rttdocumentManagement.services.document_management_core_services import DocumentManagementCoreService
from rttregulation.services.relevant_regulation_service import RelevantRegulationService
from rttnews.services.relevant_news_service import RelevantNewsService
from rttsubstance.services.relevant_substance_service import RelevantSubstanceService
from rttproduct.services.relevant_product_services import RelevantProductService
from rttcore.services.id_search_service import IdSearchService


logger = logging.getLogger(__name__)


class DocManagementFilerOptionAPIView(APIView):
    permission_classes = (IsAuthenticated, IsActiveDocumentManagementModule)

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            filters = {
                "regulatory_frameworks": request.data.get("regulatory_frameworks", None),
                "regulations": request.data.get("regulations", None),
                "products": request.data.get("products", None),
                "substances": request.data.get("substances", None),
                "news": request.data.get("news", None),
                "uploaded_by": request.data.get("uploaded_by", None),
                "from_date": request.data.get("from_date", None),
                "to_date": request.data.get("to_date", None),
            }
            search_keyword = request.data.get("search", None)
            organization_id = request.user.organization_id
            # create instance
            doc_management_service = DocumentManagementCoreService(organization_id)
            # apply main filter
            doc_management_doc_qs = doc_management_service.get_filtered_doc_management_doc_qs(filters, search_keyword)
            # take all the data
            doc_management_doc_qs = doc_management_doc_qs[0:doc_management_doc_qs.count()]
            rel_reg_service = RelevantRegulationService()
            relevant_fw_list = rel_reg_service.get_relevant_regulatory_framework_id_organization(organization_id)
            relevant_reg_list = rel_reg_service.get_relevant_regulation_id_organization(organization_id)
            rel_product_service = RelevantProductService()
            relevant_product_list = rel_product_service.get_organization_relevant_product_ids(organization_id)
            rel_news_service = RelevantNewsService()
            relevant_news_list = rel_news_service.get_organization_relevant_news_ids(organization_id)
            rel_substance_service = RelevantSubstanceService()
            relevant_substance_list = rel_substance_service.get_organization_relevant_substance_ids(organization_id)
            id_search_service = IdSearchService()
            regulatory_frameworks = []
            visited_regulatory_frameworks = {}
            regulations = []
            visited_regulations = {}
            products = []
            visited_products = {}
            substances = []
            visited_substances = {}
            news_list = []
            visited_news_list = {}
            uploaded_by = []
            visited_uploaded_by = {}
            for doc_management in doc_management_doc_qs:
                # related regulatory_frameworks
                for framework in doc_management.regulatory_frameworks:
                    if id_search_service.does_id_exit_in_sorted_list(relevant_fw_list, framework.id) and \
                            framework.id not in visited_regulatory_frameworks:
                        visited_regulatory_frameworks[framework.id] = True
                        regulatory_frameworks.append({
                            'id': framework.id,
                            'name': framework.name,
                        })
                # related regulations
                for regulation in doc_management.regulations:
                    if id_search_service.does_id_exit_in_sorted_list(relevant_reg_list, regulation.id) and\
                            regulation.id not in visited_regulations:
                        visited_regulations[regulation.id] = True
                        regulations.append({
                            'id': regulation.id,
                            'name': regulation.name,
                        })
                # related products
                for product in doc_management.products:
                    if id_search_service.does_id_exit_in_sorted_list(relevant_product_list, product.id) and \
                            product.id not in visited_products:
                        visited_products[product.id] = True
                        products.append({
                            'id': product.id,
                            'name': product.name,
                            'image': product.image,
                        })
                # related substances
                for substance in doc_management.substances:
                    if id_search_service.does_id_exit_in_sorted_list(relevant_substance_list, substance.id) and\
                            substance.id not in visited_substances:
                        visited_substances[substance.id] = True
                        substances.append({
                            'id': substance.id,
                            'name': substance.name,
                        })
                # related news
                for news in doc_management.news:
                    if id_search_service.does_id_exit_in_sorted_list(relevant_news_list, news.id) and \
                            news.id not in visited_news_list:
                        visited_news_list[news.id] = True
                        news_list.append({
                            'id': news.id,
                            'title': news.title,
                        })
                # related uploaded_by
                if doc_management.uploaded_by and doc_management.uploaded_by.id not in visited_uploaded_by:
                    visited_uploaded_by[doc_management.uploaded_by.id] = True
                    uploaded_by.append({
                        'id': doc_management.uploaded_by.id,
                        'first_name': doc_management.uploaded_by.first_name,
                        'last_name': doc_management.uploaded_by.last_name,
                        'avatar': doc_management.uploaded_by.avatar,
                    })

            response = {
                'regulatory_frameworks': regulatory_frameworks,
                'regulations': regulations,
                'products': products,
                'substances': substances,
                'news': news_list,
                'uploaded_by': uploaded_by
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
        return Response({"message": "Serve error!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
