from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.auth_middleware import LoginProfileRequiredMixin

from chat.models import Chat


class ChatView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'chat.html'
    model = Chat

    def get_context_data(self, **kwargs):
        kwargs['chat'] = self.model.objects.filter(chat_name='abc').first()
        return kwargs
