from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('document', views.DocumentView.as_view(), name='document'),
    path('search/', include('haystack.urls')),
]
