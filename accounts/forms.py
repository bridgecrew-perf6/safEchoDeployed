from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import Profile

User = get_user_model()


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'confirm password'})
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'username'})

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'username')


class ProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dob'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Date of birth'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Phone number'})
        self.fields['country'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'country'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'address'})
        self.fields['postal_code'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'postal_code'})
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'city'})
        self.fields['marketing'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'marketing'})

    class Meta:
        model = Profile
        fields = ('user', 'dob', 'phone_number', 'country', 'address', 'postal_code', 'city', 'role', 'marketing')
