from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.auth_middleware import LoginProfileRequiredMixin


# Create your views here.
class ChatView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'chat.html'
