from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rttsubstance.views.es.prioritized_substances.news.news_prioritized_substance_data import \
    NewsPrioritizedSubstanceData
from rttsubstance.views.es.prioritized_substances.news.news_prioritized_filter_option import \
    SubstanceNewsPrioritizedFilterOptions
from rttsubstance.views.es.prioritized_substances.property.property_prioritized_substance_data import \
    PropertyPrioritizedSubstanceData
from rttsubstance.views.es.substance_details.substance_data import SubstanceData
from rttsubstance.views.es.substance_header.substance_header_data import SubstanceHeaderData
from rttsubstance.views.es.substance_header.substance_header_filter_option import SubstanceHeaderFilterOptions
from rttsubstance.views.es.substance_list.substance_list_data import SubstanceListApiView
from rttsubstance.views.es.prioritized_substances.substance_related_data import SubstanceRelatedDataAPIView
from rttsubstance.views.es.prioritized_substances.regulation.regulation_prioritized_substance_data import \
    RegulationPrioritizedAPIView
from rttsubstance.views.es.prioritized_substances.regulation.regulation_prioritized_filter_option import \
    RegulationPrioritizedFilterOptions
from rttsubstance.views.model_views import PropertyViewSet, SubstanceUsesAndApplicationViewSet
from rttsubstance.views.es.latest_update.substance_latest_updates_data import SubstanceLatestUpdatesMilestoneAPIView
from rttsubstance.views.es.latest_update.substance_latest_updates_filter_option import \
    SubstanceLatestUpdatesFilterOptions
from rttsubstance.views.es.substance_details.substance_details import SubstanceDetailsAPIView
from rttsubstance.views.es.substance_details.substance_timeline_api import SubstanceTimeLine
from rttsubstance.views.es.substance_details.substance_region_topic_chart import SubstanceRegionTopicChart
from rttsubstance.views.es.substance_details.regulations.substance_regulations import SubstanceDetailsRegulations
from rttsubstance.views.es.substance_details.regulations.substance_regulations_filter_option import\
    SubstanceDetailsRegulationsFilterOptions
from rttsubstance.views.es.substance_details.news.substance_news import SubstanceNews
from rttsubstance.views.es.substance_details.news.substance_news_filter_option import SubstanceNewsFilterOptions
from rttsubstance.views.es.substance_details.milestone.substance_milestone import SubstanceMilestoneAPIView
from rttsubstance.views.es.substance_details.milestone.substance_milestone_filter_option import \
    SubstanceMilestoneFilterOption
from rttsubstance.views.es.substance_options.substance_options_product_api import SubstanceOptionsProductAPIView
from rttsubstance.views.substances_upload.substance_upload_api import SubstanceUploadAPIView
from rttsubstance.views.substances_upload.substance_upload_api import SubstanceAddAPIView
from rttsubstance.views.add_substance.all_substance_list_api_view import AllSubstanceList, AdminAllSubstanceList
from rttsubstance.views.add_substance.add_substance_manually_api_view import AddSubstanceManuallyAPIView
from rttsubstance.views.add_substance.substance_details_edit import SubstanceEdit
from rttsubstance.views.substance_add_relation.manual_substance_add_or_remove_relation import \
    ManualSubstanceAddOrRemoveRelation
from rttsubstance.views.substance_add_relation.upload_substance_add_relation import UploadSubstanceAddRelationAPIView
from rttsubstance.views.related_substance.related_substance_list_api_view import RelatedSubstanceFromRDSListAPIView
from rttsubstance.views.es.relevant_substance.rel_substance_data_inside_others_details import \
    RelSubstanceDataInsideOtherDetailsAPIView
from rttsubstance.views.admin.admin_substance_data_viewset import AdminSubstanceDataViewSet
from rttsubstance.views.admin.admin_substance_family_viewset import AdminSubstanceFamilyViewSet
from rttsubstance.views.es.prioritized_substances.property.prioritized_strategy_filter_option import\
    PrioritizedStrategyFilterOptions
from rttsubstance.views.es.latest_update.substance_latest_updates_data_news import SubstanceLatestUpdatesNewsAPIView

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'substance-uses-and-application', SubstanceUsesAndApplicationViewSet)
router.register(r'admin/substance-data', AdminSubstanceDataViewSet)
router.register(r'admin/substance-family', AdminSubstanceFamilyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('es/substance/header-data/', SubstanceHeaderData.as_view()),
    path('es/substance/header-filter-options/', SubstanceHeaderFilterOptions.as_view()),
    path('es/substance/list/', SubstanceListApiView.as_view()),
    path('es/substance/<int:substance_id>/related-data/', SubstanceRelatedDataAPIView.as_view()),
    path('es/substance/regulation-prioritized/list/', RegulationPrioritizedAPIView.as_view()),
    path('es/substance/regulation-prioritized/filter-options/', RegulationPrioritizedFilterOptions.as_view()),
    path('es/substance/news-prioritized/list/', NewsPrioritizedSubstanceData.as_view()),
    path('es/substance/news-prioritized/filter-options/', SubstanceNewsPrioritizedFilterOptions.as_view()),
    path('es/substance/property-prioritized/list/', PropertyPrioritizedSubstanceData.as_view()),
    path('es/substance/property-prioritized/list/filter-options/', PrioritizedStrategyFilterOptions.as_view()),
    path('es/substance/latest-updates/milestone/', SubstanceLatestUpdatesMilestoneAPIView.as_view()),
    path('es/substance/latest-updates/news/', SubstanceLatestUpdatesNewsAPIView.as_view()),
    path('es/substance/latest-updates/filter-options/<str:tab_name>/', SubstanceLatestUpdatesFilterOptions.as_view()),
    path('es/substance/<int:substance_id>/details/', SubstanceDetailsAPIView.as_view()),
    path('es/substance/<int:substance_id>/timeline/', SubstanceTimeLine.as_view()),
    path('es/substance/<int:substance_id>/region-topic-chart/', SubstanceRegionTopicChart.as_view()),
    path('es/substance/<int:substance_id>/regulations/', SubstanceDetailsRegulations.as_view()),
    path('es/substance/<int:substance_id>/regulations/filter-options/',
         SubstanceDetailsRegulationsFilterOptions.as_view()),
    path('es/substance/<int:substance_id>/news/', SubstanceNews.as_view()),
    path('es/substance/<int:substance_id>/news/filter-options/', SubstanceNewsFilterOptions.as_view()),
    path('es/substance/<int:substance_id>/milestones/', SubstanceMilestoneAPIView.as_view()),
    path('es/substance/<int:substance_id>/milestones/filter-options/', SubstanceMilestoneFilterOption.as_view()),
    path('es/substance/<int:substance_id>/substance-data/', SubstanceData.as_view()),
    path('es/substance/substance-options-product/', SubstanceOptionsProductAPIView.as_view()),
    path('es/substance/substances-upload/<str:process_type>/', SubstanceUploadAPIView.as_view()),
    path('es/substance/<str:process_type>/', SubstanceAddAPIView.as_view()),
    path('add-substance-manually/', AddSubstanceManuallyAPIView.as_view()),
    path('all-substance-list/', AllSubstanceList.as_view()),
    path('substance/<int:substance_id>/edit/', SubstanceEdit.as_view()),
    path('substance/manual-add-or-remove-relation/', ManualSubstanceAddOrRemoveRelation.as_view()),
    path('substance/upload-substance-add-relation/', UploadSubstanceAddRelationAPIView.as_view()),
    path('related-substance-list/', RelatedSubstanceFromRDSListAPIView.as_view()),
    path('es/relevant-substance-data/<int:data_id>/', RelSubstanceDataInsideOtherDetailsAPIView.as_view()),
]

admin_urlpatterns = [
    path('admin/all-substance-list/', AdminAllSubstanceList.as_view()),
]

urlpatterns += admin_urlpatterns
