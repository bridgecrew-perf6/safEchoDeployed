from django.db import models
from accounts.models import Profile


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class GPTApi(BaseModel):
    GPT_3 = 'gpt_3'
    GPT_j = 'gpt_j'
    GPT_CHOICES = (
        (GPT_3, 'GPT - 3'),
        (GPT_j, 'GPT - j'),
    )
    name = models.CharField(max_length=25, unique=True)
    type = models.CharField(max_length=20, choices=GPT_CHOICES, default=GPT_j)
    key = models.CharField(max_length=750)
    url = models.URLField()

    def __str__(self):
        return f"{self.name}"


class Bot(BaseModel):
    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=300)
    logo = models.ImageField(upload_to='bot_logo/')
    application = models.DateTimeField(auto_now_add=True)
    api = models.ForeignKey(GPTApi, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.name}"


class Engine(BaseModel):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return f"{self.name}"


class GPTPrompt(BaseModel):
    name = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=300)
    prompt = models.JSONField()
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE)
    temperature = models.FloatField()
    max_tokens = models.IntegerField()
    top_p = models.FloatField()
    frequency_penalty = models.FloatField()
    Presence_penalty = models.FloatField()
    stop = models.JSONField()

    def __str__(self):
        return f"{self.name}"


class Conversation(BaseModel):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, unique=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class ConversationContent(BaseModel):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    query = models.TextField()
    response = models.TextField(null=True)
    response_json = models.JSONField(null=True)

    def __str__(self):
        return f"{self.sender}"
