from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rttdocument.views.views import DocumentViewSet, DocumentTypeViewSet, HelpApiView

router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
router.register(r'document-type', DocumentTypeViewSet)
router.register(r'help', HelpApiView)

urlpatterns = [
    path('', include(router.urls)),
]
