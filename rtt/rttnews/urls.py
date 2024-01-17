from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rttnews.views.es.news_details_api import NewsDetailsApiView, RelatedNewsListApiView
from rttnews.views.news_api_view import NewsViewSet, NewsCategoryViewSet, NewsSourceViewSet, NewsRelevanceViewSet, \
    SourceTypeViewSet, NewsAssessmentWorkflowViewSet, NewsAnswerViewSet, NewsQuestionViewSet
from rttnews.views.news_search_api import DashboardRightChartApiView, DashboardTimelineApiView, \
    DashboardFilterOptionsApiView, DashboardContentApiView
from rttnews.views.news_impact_assessment_display.news_impact_assessment_api_view import \
    NewsImpactAssessmentQuestionListAPIView, NewsImpactAssessmentAnswerListAPIView
from rttnews.views.impact_rating_task_history.impact_rating_task_history_api_view import ImpactRatingTaskHistory
from rttnews.views.generate_default_news_question.generate_default_news_question_api_view import \
    GenerateDefaultNewsQuestionAPIView
from rttnews.views.admin_management.add_new_assessment_api_view import NewAssessmentBulkAddAdminAPIView
from rttnews.views.map_view.dashboard_map_api_view import DashBoardMapAPIView
from rttnews.views.dashboard_content_view_lazy_load import DashboardContentLazyLoadApiView
from rttnews.views.remove_existing_news_api import RemoveExistingNewsIrrelevantToOrganization
from rttnews.views.report_module.news_report_api_view import NewsReportAPIView
from rttnews.views.report_module.news_report_filter_options import NewsReportFilterOptionsApiView
from rttnews.views.report_module.news_report_insight_chart import NewsReportInsightChart
from rttnews.views.restore_news_assessment_workflow_script import RestoreNewsAssessmentWorkflowScript
from rttnews.views.news_body_valid_link_gen import NewsBodyValidLinkGenAPIView

router = DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'news-category', NewsCategoryViewSet)
router.register(r'news-source', NewsSourceViewSet)
router.register(r'news-relevance', NewsRelevanceViewSet)
router.register(r'source-type', SourceTypeViewSet)
router.register(r'news-assessment-workflow', NewsAssessmentWorkflowViewSet)
router.register(r'news-impact-assessment-answer', NewsAnswerViewSet)
router.register(r'news-impact-assessment-question', NewsQuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('es/dashboard-right-chart/', DashboardRightChartApiView.as_view(), name='es_dashboard_right_chart'),
    path('es/dashboard-content/', DashboardContentApiView.as_view(), name='es_dashboard_content'),
    path('es/dashboard-timeline/', DashboardTimelineApiView.as_view(), name='es_dashboard_timeline'),
    path('es/dashboard-filter-options/', DashboardFilterOptionsApiView.as_view(), name='es_dashboard_filter'),
    path('es/news-details/<int:news_id>', NewsDetailsApiView.as_view(), name='es_news_details'),
    path('es/news/<int:news_id>/related-news', RelatedNewsListApiView.as_view(), name='es_related_news'),
    path('news/impact-assessment-question/list/', NewsImpactAssessmentQuestionListAPIView.as_view(),
         name='news_question_list'),
    path('news/impact-assessment-answer/list/', NewsImpactAssessmentAnswerListAPIView.as_view(),
         name='news_answer_list'),
    path('impact-rating-task-history-list/', ImpactRatingTaskHistory.as_view(), name='impact_rating_task_history'),
    path('generate-default-news-question/', GenerateDefaultNewsQuestionAPIView.as_view()),
    path('bulk-add-new-assessment/<int:news_id>/', NewAssessmentBulkAddAdminAPIView.as_view(),
         name='add_new_assessment_admin_site'),
    path('es/news/<int:news_id>/related-news', RelatedNewsListApiView.as_view(), name='es_related_news'),
    path('es/dashboard-map-view/', DashBoardMapAPIView.as_view(), name='dashboard_map_view'),
    path('es/dashboard-content/lazy-loaded/', DashboardContentLazyLoadApiView.as_view(),
         name='es_dashboard_content_lazy_load'),
    path('remove-irrelevant-news-assessment-workflow/', RemoveExistingNewsIrrelevantToOrganization.as_view(),
         name='remove_irrelevant_news_assessment_workflow'),
    path('es/news-report/', NewsReportAPIView.as_view(), name='es_news_report'),
    path('es/news-report/filter-options/', NewsReportFilterOptionsApiView.as_view(),
         name='es_news_report_filter_options'),
    path('es/news-report/insight-chart/', NewsReportInsightChart.as_view(), name='es_news_report_insight_chart'),
    path('es/restore-new-assessment-workflow-script/', RestoreNewsAssessmentWorkflowScript.as_view()),
    path('news-body-valid-link/<int:news_id>/', NewsBodyValidLinkGenAPIView.as_view()),
]
