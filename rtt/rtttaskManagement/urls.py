from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rtttaskManagement.views.task_api_view import TaskViewSet
from rtttaskManagement.views.task_comment_api_view import TaskCommentViewSet
from rtttaskManagement.views.es.task_list.task_list_api_view import TaskListAPIView
from rtttaskManagement.views.es.task_list.task_list_filter_options import TaskListFilterOptionAPIView
from rtttaskManagement.views.es.task_create_update_filter_option.task_create_update_filter_options import \
    TaskCreateEditFilterOption
from rtttaskManagement.views.es.details_page.news.news_details_task_data import TaskListInNewsDetails
from rtttaskManagement.views.es.details_page.regulation.regulation_details_task_data import TaskListInRegulationDetails
from rtttaskManagement.views.es.details_page.framework.framework_details_task_data import TaskListInFrameworkDetails
from rtttaskManagement.views.es.details_page.substance.substance_details_task_data import TaskListInSubstanceDetails
from rtttaskManagement.views.es.details_page.product.product_details_task_data import TaskListInProductDetails

router = DefaultRouter()
router.register(r'task', TaskViewSet)
router.register(r'task-comment', TaskCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('es/task/list/', TaskListAPIView.as_view()),
    path('es/task/list/filter-options/', TaskListFilterOptionAPIView.as_view()),
    path('es/task/create-edit-dropdown-options/', TaskCreateEditFilterOption.as_view()),
    path('es/task/news-details/<int:news_id>/', TaskListInNewsDetails.as_view()),
    path('es/task/regulation-details/<int:regulation_id>/', TaskListInRegulationDetails.as_view()),
    path('es/task/framework-details/<int:framework_id>/', TaskListInFrameworkDetails.as_view()),
    path('es/task/substance-details/<int:substance_id>/', TaskListInSubstanceDetails.as_view()),
    path('es/task/product-details/<int:product_id>/', TaskListInProductDetails.as_view()),
]
