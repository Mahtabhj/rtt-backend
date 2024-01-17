from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rttdocumentManagement.views.es.doc_management_list.doc_management_data import DocManagementAPIView
from rttdocumentManagement.views.es.doc_management_list.doc_management_filter_options import \
    DocManagementFilerOptionAPIView
from rttdocumentManagement.views.document_management_api_view import DocumentManagementViewSet
from rttdocumentManagement.views.es.dropdown_options_api_view import DocManagementCreateEditDropdownOptionsAPIView
from rttdocumentManagement.views.doc_management_comment_viewset import DocumentManagementCommentViewSet

router = DefaultRouter()
router.register(r'document-managements', DocumentManagementViewSet)
router.register(r'doc-management-comments', DocumentManagementCommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('es/doc-management-data-list/', DocManagementAPIView.as_view()),
    path('es/doc-management-data-list/filter-option/', DocManagementFilerOptionAPIView.as_view()),
    path('es/doc-management/create-edit-dropdown-options/', DocManagementCreateEditDropdownOptionsAPIView.as_view()),
]
