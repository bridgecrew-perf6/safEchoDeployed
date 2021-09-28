from django.contrib import admin
from .models import User, Profile


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name']
    ordering = ['id']
    search_fields = ['id', 'email']


@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_email']
    ordering = ['id']
    search_fields = ['id', 'user']

    def get_email(self, obj):
        return obj.email
