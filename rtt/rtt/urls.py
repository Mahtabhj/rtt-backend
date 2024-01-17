from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rttadmin import urls as admin_urls
from rttorganization import urls as organization_urls
from rttdocument import urls as document_urls
from rttauth import urls as auth_urls
from rttnews import urls as news_urls
from rttproduct import urls as product_urls
from rttregulation import urls as regulations_urls
from rttcore import urls as core_urls
from rttnotification import urls as notification_urls
from rttsubstance import urls as substance_urls
from rttpublicApi import urls as public_api_urls
from rttlimitManagement import urls as limit_management_urls
from rtttaskManagement import urls as task_management_urls
from rttdocumentManagement import urls as document_management_urls
from rttcore.swagger_config import Swagger
from rest_framework import permissions

urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('backend/api/', include(organization_urls)),
    path('backend/api/', include(auth_urls)),
    path('backend/api/', include(news_urls)),
    path('backend/api/', include(product_urls)),
    path('backend/api/', include(regulations_urls)),
    path('backend/api/', include(document_urls)),
    path('backend/api/', include(core_urls)),
    path('backend/api/', include(notification_urls)),
    path('backend/api/', include(substance_urls)),
    path('backend/api/', include(limit_management_urls)),
    path('backend/api/', include(task_management_urls)),
    path('backend/api/', include(document_management_urls)),
]

privateUrlpatterns = [path('backend/public-api/', include(public_api_urls))]

'''
    Swagger configuration
'''
swagger = Swagger(version='01', title='RTT API', is_public=True, all_permissions=(), patterns=urlpatterns)
swagger_urls = swagger.get_swagger_url()

urlpatterns = urlpatterns + privateUrlpatterns + swagger_urls + admin_urls.urlpatterns
