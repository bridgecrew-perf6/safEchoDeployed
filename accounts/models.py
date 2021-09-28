from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    USER = 'user'
    EXPERT = 'expert'
    HR = 'hr'
    KNOWLEDGE_OWNER = 'knowledge_owner'
    ROLES = (
        (USER, 'User'),
        (EXPERT, 'Expert'),
        (HR, 'HR'),
        (KNOWLEDGE_OWNER, 'Knowledge Owner'),
    )
    SEARCH_ENGINE = 'search_engine'
    FRIENDS = 'friends'
    SOCIAL_MEDIA = 'social_media'
    BLOG = 'blog'
    CONFERENCE = 'conference'
    OTHER = 'other'
    MARKETING = (
        (SEARCH_ENGINE, 'Search Engine (Google, Yahoo, etc)'),
        (FRIENDS, 'Recommended by friend or colleague '),
        (SOCIAL_MEDIA, 'Social Media '),
        (BLOG, 'Blog or Publications '),
        (CONFERENCE, 'Conference'),
        (OTHER, 'Other:..'),
    )
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    dob = models.DateField()
    phone_number = PhoneNumberField(unique=True)
    country = CountryField()
    address = models.CharField(max_length=850)
    postal_code = models.CharField(max_length=100)
    city = models.CharField(max_length=255)
    role = models.CharField(choices=ROLES, max_length=50, default=USER)
    marketing = models.CharField(choices=MARKETING, max_length=50)

    def __str__(self):
        return self.user.email
