from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rttproduct.views.es.product_details_api import ProductDetailsApiView
from rttproduct.views.es.product_list_api import ProductsListApiView, ProductListFilterOptionsApiView
from rttproduct.views.es.product_options_api import ProductCategoryOptionsApiView, MaterialCategoryOptionsApiView, \
    ProductOptionsApiView
from rttproduct.views.es.product_related_frameworks_api import ProductRelatedFrameworksApiView, \
    ProductDetailFilterOptionsApiView
from rttproduct.views.es.product_related_news_api import ProductRelatedNewsApiView,\
    ProductRelatedNewsFilterOptionsApiView
from rttproduct.views.product_api_view import (ProductViewSet, IndustryViewSet, ProductCategoryViewSet,
                                               MaterialCategoryViewSet,)
from rttproduct.views.product_search_api import DashboardKeyFiguresApiView
from rttproduct.views.es.product_related_substance_api import ProductRelatedSubstancesApiView, \
    AllProductRelatedSubstancesIdApiView
from rttproduct.views.es.product_details_page.related_substances import ProductDetailsRelSubstance

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'industries', IndustryViewSet)
router.register(r'product-categories', ProductCategoryViewSet)
router.register(r'material-categories', MaterialCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('es/dashboard-key-figures/', DashboardKeyFiguresApiView.as_view(), name='es_dashboard_key_figures'),
    path('es/product-list/', ProductsListApiView.as_view(), name='es_product_list'),
    path('es/product-list-filter-options/', ProductListFilterOptionsApiView.as_view(),
         name='es_product_list_filter_options'),
    path('es/product-category-options/', ProductCategoryOptionsApiView.as_view(), name='es_product_category_options'),
    path('es/material-category-options/', MaterialCategoryOptionsApiView.as_view(),
         name='es_material_category_options'),
    path('es/product-options/', ProductOptionsApiView.as_view(), name='es_product_options'),
    path('es/product-details/<int:product_id>', ProductDetailsApiView.as_view(), name='es_product_details'),
    path('es/product-detail-filter-options/<int:product_id>', ProductDetailFilterOptionsApiView.as_view(),
         name='es_product_detail_filter_options'),
    path('es/product/<int:product_id>/related-news/', ProductRelatedNewsApiView.as_view(),
         name='es_product_related_news'),
    path('es/product/<int:product_id>/related-news-filter-options/', ProductRelatedNewsFilterOptionsApiView.as_view(),
         name='es_product_related_news'),
    path('es/product/<int:product_id>/related-frameworks/', ProductRelatedFrameworksApiView.as_view(),
         name='es_product_related_frameworks'),
    path('es/product/<int:product_id>/related-substances/', ProductRelatedSubstancesApiView.as_view(),
         name='es_product_related_substance'),
    path('es/product/<int:product_id>/all-related-substances-id/', AllProductRelatedSubstancesIdApiView.as_view(),
         name='es_all_product_related_substance_id'),
    path('es/product-details/<int:product_id>/substances/', ProductDetailsRelSubstance.as_view()),
]
