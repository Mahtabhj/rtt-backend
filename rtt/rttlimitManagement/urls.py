from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rttlimitManagement.views.limit_upload.limit_upload_api import LimitUploadAPIView
from rttlimitManagement.views.model_views import LimitAttributeViewSet

from rttlimitManagement.views.es.limt_list.limit_list_api import LimitListAPIView
from rttlimitManagement.views.es.limt_list.limit_regulation_group_by_region import LimitRegulationGroupByRegion
from rttlimitManagement.views.es.limt_list.limit_list_filter_option import LimitListFilterOption
from rttlimitManagement.views.es.limt_list.substances_limit_filter_option import SubstanceLimitFilterOption

from rttlimitManagement.views.es.exemption.limit_exemption_api import LimitExemptionAPIView
from rttlimitManagement.views.es.details_page.substance_details_page.limit_data_in_substance_details import \
    LimitInSubstanceDetails
from rttlimitManagement.views.es.details_page.substance_details_page.limit_data_filter_option_in_substance_details \
    import LimitInSubstanceDetailsFilterOption

from rttlimitManagement.views.es.details_page.framework_details_page.limit_data_in_framework_details import \
    LimitInFrameworkDetails

from rttlimitManagement.views.es.details_page.regulation_details_page.regulation_details_page_limit_data import \
    LimitInRegulationDetails
from rttlimitManagement.views.admin_site_view.limit_data.admin_limit_view import AdminLimitViewSet
from rttlimitManagement.views.admin_site_view.limit_data.regulation_limit_attribute_options import \
    RegulationLimitAttributeOptionAPIView
from rttlimitManagement.views.admin_site_view.exemption_data.admin_exemption_view import AdminExemptionViewSet
from rttlimitManagement.views.admin_site_management_view.limit_data.delete_limits_api_view import LimitDeleteAPIView
from rttlimitManagement.views.es.details_page.product_details_page.limit_data_in_product_details import\
    LimitInProductDetails
from rttlimitManagement.views.es.details_page.product_details_page.limit_data_filter_option_in_product_details import\
    LimitDataFilterOption

router = DefaultRouter()
router.register(r'limit-attributes', LimitAttributeViewSet)
router.register(r'admin/limit', AdminLimitViewSet)
router.register(r'admin/exemption', AdminExemptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('limit/limit-upload/<str:process_type>/', LimitUploadAPIView.as_view()),
    path('es/limit/list/', LimitListAPIView.as_view()),
    path('es/limit/regulation-group-by-region/', LimitRegulationGroupByRegion.as_view()),
    path('es/limit/list/filter-options/', LimitListFilterOption.as_view()),
    path('es/limit/list/substance-filter-options/', SubstanceLimitFilterOption.as_view()),
    path('es/limit/exemption/', LimitExemptionAPIView.as_view()),
    path('es/limit/substance-details/<int:substance_id>/', LimitInSubstanceDetails.as_view()),
    path('es/limit/substance-details/<int:substance_id>/filter-options/',
         LimitInSubstanceDetailsFilterOption.as_view()),
    path('es/limit/framework-details/<int:framework_id>/', LimitInFrameworkDetails.as_view()),
    path('es/limit/regulation-details/<int:regulation_id>/', LimitInRegulationDetails.as_view()),
    path('limit/attribute-options/', RegulationLimitAttributeOptionAPIView.as_view()),
    path('delete-limit/', LimitDeleteAPIView.as_view()),
    path('es/limit/product-details/<int:product_id>/', LimitInProductDetails.as_view()),
    path('es/limit/product-details/<int:product_id>/filter-options/', LimitDataFilterOption.as_view()),
]
