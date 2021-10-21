from django.contrib import admin

# Register your models here.
from chat.models import Conversation, ConversationContent,Bot


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Conversation._meta.fields]
    ordering = ['id']
    list_display_links = ['id']
    search_fields = ('name',)


@admin.register(ConversationContent)
class ConversationContentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ConversationContent._meta.fields]
    ordering = ['id']
    list_display_links = ['id']
    search_fields = ('sender',)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bot._meta.fields]
    ordering = ['id']
    list_display_links = ['id']
    search_fields = ('name',)


