from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rttpublicApi.views.add_substance import AddSubstanceApi
from rttpublicApi.views.regulatory_framework import RegulatoryFrameworkApi
from rttpublicApi.views.uses_and_applications import UsesAndApplicationsApi
from rttpublicApi.views.validate_key_secret import ValidateKeySecretApi
from rttpublicApi.views.regulation_limit_list_api import RegulationLimitPublicApi
from rttpublicApi.views.exemption_public_api import ExemptionPublicApi
from rttpublicApi.views.substance_public_api import SubstancePublicApi

router = DefaultRouter()

# router.register(r'regulatory-framework', name)

urlpatterns = [
    path('', include(router.urls)),
    path('validate-key-secret/', ValidateKeySecretApi.as_view()),
    path('regulatory-frameworks/', RegulatoryFrameworkApi.as_view()),
    path('uses-and-applications/', UsesAndApplicationsApi.as_view()),
    path('regulation-limits/', RegulationLimitPublicApi.as_view()),
    path('exemptions/', ExemptionPublicApi.as_view()),
    path('add-substance/', AddSubstanceApi.as_view()),
    path('substances/', SubstancePublicApi.as_view()),
]
