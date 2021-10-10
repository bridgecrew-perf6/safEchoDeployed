from django.db import models
from accounts.models import Profile


class ChatContent(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=256, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class Chat(models.Model):
    chat_name = models.CharField(blank=True, null=True, max_length=256, unique=True)
    chat_content = models.ManyToManyField(ChatContent)
