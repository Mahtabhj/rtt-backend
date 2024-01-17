from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rttnotification.views import NotificationAlertViewSet

router = DefaultRouter()
router.register(r'user-notifications', NotificationAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]