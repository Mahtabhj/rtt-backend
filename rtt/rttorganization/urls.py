from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rttorganization.views import organization_api_view
from rttorganization.views.search_views.organization_search_view import OrganizationApiView

router = DefaultRouter()
router.register(r'organizations', organization_api_view.OrganizationViewSet)
router.register(r'subscriptions', organization_api_view.SubscriptionViewSet)
router.register(r'subscription-type', organization_api_view.SubscriptionTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('es-organization/', OrganizationApiView.as_view(), name='es_organization'),
]
