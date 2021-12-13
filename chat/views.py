import re

from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.auth_middleware import LoginProfileRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from chat.models import Conversation, ConversationContent, Bot
from .bot import get_gpt_j_bot_response
# from .bot import BotManagement
from .bot_config import BotManagement
from .forms import ConversationForm
from django.urls import reverse


class ChatView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'chat.html'


class GetChatListView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'tabs/chat/bot_chat_tab_list.html'
    model = Conversation

    def get(self, request, *args, **kwargs):
        chats = self.model.objects.all().order_by('-created_at')
        context = {'chats': chats}
        data = dict()
        data['html_chat_list'] = render_to_string(self.template_name, context, request=request)
        active_chat = chats.first()
        data['id'] = active_chat.id
        data['chat_id'] = 'chat_' + str(active_chat.id)
        data['url'] = reverse('get_chat_content', kwargs={'pk': active_chat.id})
        return JsonResponse(data)


class GetChatContentView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'content/chat/bot_chat_content_async.html'
    model = ConversationContent

    def get(self, request, *args, **kwargs):
        chats = ConversationContent.objects.filter(conversation__id=kwargs['pk'])
        context = {'chats': chats}
        data = dict()
        data['html_chat_content'] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)


class CreateConversationView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'forms/create_new_conversation.html'
    model = ConversationContent
    form = ConversationForm

    def get(self, request, *args, **kwargs):
        form = self.form(initial={'user': request.user})
        context = {'form': form}
        data = dict()
        data['html_new_chat_form'] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = dict()
        # import pdb;pdb.set_trace()
        form = self.form(request.POST)
        form.instance.user = self.request.user.profile
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
            context = {'form': form}
            data['html_new_chat_form'] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)


class SendMessageView(LoginProfileRequiredMixin, TemplateView):
    template_name = 'content/chat/bot_send_messsage_response.html'
    model = ConversationContent

    def post(self, request, *args, **kwargs):
        query = request.POST.get('message')
        conversation = get_object_or_404(Conversation, pk=kwargs['coversation_id'])
        chat = ConversationContent(conversation=conversation, query=query,
                                   sender=request.user.profile)
        response_status, text_response, json_response, gtp3_type = BotManagement(conversation).search(query)
        if response_status == 200:
            chat.response = text_response
            chat.response_json = json_response
            chat.save()

        context = {'chat': chat, 'gtp3_type': gtp3_type}
        data = dict()
        data['html_chat_response'] = render_to_string(self.template_name, context, request=request)
        return JsonResponse(data)
