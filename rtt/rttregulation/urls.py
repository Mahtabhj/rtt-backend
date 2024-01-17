from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rttregulation.views.es.framework_details_api import RegulatoryFrameworkDetailApiView
from rttregulation.views.es.regulation_details_api import RegulationDetailApiView
from rttregulation.views.es.search_api import SearchApiView
from rttregulation.views.regulation_search_api import DashboardMilestoneSearchApi, RegulatoryFrameworkContentApiView, \
    RegulatoryFrameworkFilterOptionsApiView, RegulationUpdates
from rttregulation.views.es.what_next_regulation.milestone_data_api_view import WhatNextMilestoneAPIView
from rttregulation.views.es.what_next_regulation.milestone_data_filter_option import WhatNextMilestoneFilterOption
from rttregulation.views.regulation_impact_assessment_display.regulation_impact_assessment_api_view import \
    RegulationImpactAssessmentQuestionListAPIView, RegulationImpactAssessmentAnswerListAPIView
from rttregulation.views.views import (LanguageViewSet, StatusViewSet, RegionViewSet, UrlViewSet, IssuingBodyViewSet,
                                       RegulationViewSet, RegulationTypeViewSet, RegulatoryFrameworkViewSet,
                                       MilestoneViewSet, QuestionTypeViewSet, ImpactAssessmentQuestion,
                                       ImpactAssessmentAnswer, RegulatoryFrameworkUrlApiView, ImpactAssessmentApiView,
                                       ImpactAssessmentListApiView, TopicViewSet, RegulationRatingViewSet,
                                       RegulatoryFrameworkRatingViewSet, MilestoneTypeViewSet,
                                       ImpactAssessmentAnswerListCreateView)
from rttregulation.views.es.milestone_in_regulation_details.milestone_data_api_view import MilestoneInRegulationDetails
from rttregulation.views.es.milestone_in_regulation_details.milestone_filter_option import \
    MilestoneInRegulationDetailsFilterOption
from rttregulation.views.es.regulation_page_content.regulation_page_content_group_by_data import \
    RegulatoryFrameworkContentGroupByData
from rttregulation.views.export_regulatory_data.export_regulatory_data_api_view import \
    ExportRegulatoryDataAPIView
from rttregulation.views.map_view.regulation_map_view import RegulationMapAPIView
from rttregulation.views.regulation_mute_unmute_api_view import RegulationMuteUnmuteAPIView
from rttregulation.views.region_module.region_details_data.region_details_api_view import RegionDetailsApiView
from rttregulation.views.region_module.region_list.region_list_api_view import RegionListApiView
from rttregulation.views.region_module.published_regions.published_regions_api_view import ActiveRegionPagesApiView
from rttregulation.views.region_module.filtering_option.filtering_option_api_view import RegionPageFilterOptionApiView
from rttregulation.views.region_module.region_timeline.region_timeline_api import RegionTimeLine
from rttregulation.views.region_module.regulation_tab_list.regulation_tab_list_api_view import RegulationTabListData
from rttregulation.views.region_module.regulation_tab_list.regulation_tab_filter_option import RegulationTabFilterOption
from rttregulation.views.region_module.news_tab.news_tab_list_api_view import NewsTabListData
from rttregulation.views.region_module.news_tab.news_tab_filter_option import NewsTabFilterOption
from rttregulation.views.region_module.milestone_tab.milestone_tab_list_api_view import MilestoneTablListData
from rttregulation.views.region_module.insights_chart.insights_chart_api_view import InsightsChartApiView
from rttregulation.views.milestone_mute_unmute_api_view import MilestoneMuteUnmuteAPIView
from rttregulation.views.region_module.limit_tab.limit_tab_list_api_view import LimitTablListData
from rttregulation.views.region_module_admin.region_page_list import ReactAdminRegionPageApiView
from rttregulation.views.region_module.limit_tab.limit_tab_filter_options import LimitTabFilterOption
from rttregulation.views.regulatory_framework_content_api_view import RegulatoryFrameworkTabularContentApiView
from rttregulation.views.framework_group_by_list_data_tabular_formay import FrameworkContentGroupByDataTabularFormat
from rttregulation.views.es.what_next_regulation.milestone_data_download_excel_file import\
    ExportMilestoneDataAPIView
from rttregulation.views.regulation_tagged_product_cat_material_cat import RegulationTaggedProductCatMaterialCatAPIView
from rttregulation.views.map_view.whats_next_map_api_view import WhatsNextMapAPIView

router = DefaultRouter()

router.register(r'regulatory-framework', RegulatoryFrameworkViewSet)
router.register(r'milestone', MilestoneViewSet)
router.register(r'issuing-body', IssuingBodyViewSet)
router.register(r'regulation', RegulationViewSet)
router.register(r'impact-assessment-question', ImpactAssessmentQuestion)
router.register(r'impact-assessment-answer', ImpactAssessmentAnswer)
router.register(r'url', UrlViewSet)
router.register(r'topic', TopicViewSet)
router.register(r'regulation-rating', RegulationRatingViewSet)
router.register(r'regulatory-framework-rating', RegulatoryFrameworkRatingViewSet)
router.register(r'milestone-type', MilestoneTypeViewSet)
router.register(r'question-type', QuestionTypeViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'status', StatusViewSet)
router.register(r'region', RegionViewSet)
router.register(r'regulation-type', RegulationTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reg-framework-url/', RegulatoryFrameworkUrlApiView.as_view(), name='reg_framework_url'),
    path('impact-assessment/', ImpactAssessmentApiView.as_view(), name='impact_assessment'),
    path('impact-assessments/', ImpactAssessmentListApiView.as_view(), name='impact_assessments'),
    path('impact-assessment-answer-list/', ImpactAssessmentAnswerListCreateView.as_view(),
         name='impact_assessment_answer_list'),
    path('es/milestone/', DashboardMilestoneSearchApi.as_view(), name='es_regulation'),
    path('es/regulatory-framework-content/', RegulatoryFrameworkContentApiView.as_view(),
         name='es_regulatory_framework_content'),
    path('es/regulatory-framework-filter/', RegulatoryFrameworkFilterOptionsApiView.as_view(),
         name='es_regulatory_framework_filter'),
    path('es/regulation-updates/', RegulationUpdates.as_view(), name='es_regulation_updates'),
    path('es/regulatory-framework-details/<int:framework_id>', RegulatoryFrameworkDetailApiView.as_view(),
         name='es_regulatory_framework_details'),
    path('es/regulation-details/<int:regulation_id>', RegulationDetailApiView.as_view(),
         name='es_regulation_details'),
    path('es/search', SearchApiView.as_view(), name='es_search'),
    path('es/regulation-milestone/', MilestoneInRegulationDetails.as_view(),
         name='milestone_in_regulation_details'),
    path('es/regulation-milestone-filter-options/', MilestoneInRegulationDetailsFilterOption.as_view(),
         name='regulation_milestone_filter_options'),
    path('es/regulation/what-next/', WhatNextMilestoneAPIView.as_view(), name='es_what_next_milestone'),
    path('es/regulation/what-next-filter-options/', WhatNextMilestoneFilterOption.as_view(),
         name='es_what_next_milestone_filter_options'),
    path('es/regulatory-framework-content/group-by-data-list/', RegulatoryFrameworkContentGroupByData.as_view()),
    path('export-regulatory-data/', ExportRegulatoryDataAPIView.as_view()),
    path('es/regulation-map-view/', RegulationMapAPIView.as_view()),
    path('regulation/impact-assessment-question/list/', RegulationImpactAssessmentQuestionListAPIView.as_view(),
         name='regulation_question_list'),
    path('regulation/impact-assessment-answer/list/', RegulationImpactAssessmentAnswerListAPIView.as_view(),
         name='regulation_answer_list'),
    path('regulation-mute-unmute/', RegulationMuteUnmuteAPIView.as_view(), name='regulation_mute_unmute'),
    path('milestone-mute-unmute/', MilestoneMuteUnmuteAPIView.as_view(), name='milestone_mute_unmute'),
    path('es/regulatory-framework-tabular-content/', RegulatoryFrameworkTabularContentApiView.as_view(),
         name='es_regulatory_framework_tabular_content'),
    path('es/tabular-format-framework-content/group-by-data-list/', FrameworkContentGroupByDataTabularFormat.as_view()),
    path('export-milestone-data/', ExportMilestoneDataAPIView.as_view()),
    path('regulation-tagged-product-cat-material-cat/', RegulationTaggedProductCatMaterialCatAPIView.as_view()),
    path('es/whats-next-map-view/', WhatsNextMapAPIView.as_view(), name='whats_next_map_view'),
]

region_module_urlpatterns = [
    path('es/region-details/<int:region_id>/', RegionDetailsApiView.as_view(), name='region_details'),
    path('es/region-list/', RegionListApiView.as_view(), name='region_list'),
    path('es/active-region-pages/', ActiveRegionPagesApiView.as_view(), name='active_region_pages'),
    path('es/region/<int:region_id>/header-filter-options/', RegionPageFilterOptionApiView.as_view(),
         name='region_page_filter_options'),
    path('es/region/<int:region_id>/timeline/', RegionTimeLine.as_view()),
    path('es/region/<int:region_id>/regulation-data/', RegulationTabListData.as_view(), name='regulation_tab_list'),
    path('es/region/<int:region_id>/regulation-data/filter-options/', RegulationTabFilterOption.as_view(),
         name='regulation_filter_option'),
    path('es/region/<int:region_id>/news-data/', NewsTabListData.as_view()),
    path('es/region/<int:region_id>/news-data/filter-options/', NewsTabFilterOption.as_view()),
    path('es/region/<int:region_id>/milestone-data/', MilestoneTablListData.as_view(), name='milestone_tab_data'),
    path('es/region/<int:region_id>/insights-chart/', InsightsChartApiView.as_view(), name='insights_chart'),
    path('es/region/<int:region_id>/limit-data/', LimitTablListData.as_view(), name='limit_tab_data'),
    path('es/region/<int:region_id>/limit-data/filter-options/', LimitTabFilterOption.as_view(),
         name='limit_filter_option'),
]

urlpatterns += region_module_urlpatterns


react_admin_region_module_urlpatterns = [
    path('es/react-admin-active-region-page/', ReactAdminRegionPageApiView.as_view(), name='region_page_list'),
]

urlpatterns += react_admin_region_module_urlpatterns
