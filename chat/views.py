from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.auth_middleware import LoginProfileRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse

from chat.models import Chat


class ChatView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'chat.html'


class GetChatListView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'tabs/chat/bot_chat_tab_list.html'
    model = Chat

    def get(self, request, *args, **kwargs):
        chats = self.model.objects.all()
        context = {'chats': chats}
        data = dict()
        data['html_chat_list'] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)


class GetChatContentView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'content/chat/bot_chat_content_async.html'
    model = Chat

    def get(self, request, *args, **kwargs):
        chat = get_object_or_404(self.model, pk=kwargs['pk'])
        context = {'chat': chat}
        data = dict()
        data['html_chat_content'] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)
