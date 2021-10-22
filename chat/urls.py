from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('chat', views.ChatView.as_view(), name='chat'),
    path('get_chat_content/<int:pk>/', views.GetChatContentView.as_view(), name='get_chat_content'),
    path('get_chat_list/', views.GetChatListView.as_view(), name='get_chat_list'),
    path('create_chat/', views.CreateConversationView.as_view(), name='create_chat'),
    path('send_message/<int:coversation_id>/', views.SendMessageView.as_view(), name='send_message'),
]
