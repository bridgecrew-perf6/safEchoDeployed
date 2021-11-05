from django.contrib import admin
from .models import User, Profile
from django import forms


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if len(self.cleaned_data["password"]) < 16:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserCreationForm
    list_display = ['id', 'email', 'first_name', 'last_name']
    ordering = ['id']
    search_fields = ['id', 'email']


@admin.register(Profile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    ordering = ['id']
    search_fields = ['id', 'user']

    # def get_email(self, obj):
    #     return user.email
