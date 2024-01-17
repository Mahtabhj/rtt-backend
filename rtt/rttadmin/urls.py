from django.urls import path, re_path
from rttadmin.views import views

urlpatterns = [
    re_path(r'^backend/.*', views.index, name='react'),
    # path('', views.index, name='react'),
]