from django.urls import path

from rttcore.views.rating_data_generator import RatingDataGenerator
from rttcore.views.views import ElasticSearchRebuild, ElasticSearchPopulate
from rttcore.views.permissions.permission_api_view import UserPermissionAPIView

urlpatterns = [
    path('es-data/rebuild/', ElasticSearchRebuild.as_view()),
    path('es-data/populate/', ElasticSearchPopulate.as_view()),
    path('user-permissions/', UserPermissionAPIView.as_view()),
    path('rating-data-generator/', RatingDataGenerator.as_view()),
]
