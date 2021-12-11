from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('document', views.DocumentView.as_view(), name='document'),
    path('document_excel', views.DocumentExcelView.as_view(), name='document_excel'),
    path('search/', include('haystack.urls')),
]
