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
        # self.fields['username'].widget.attrs.update(
        #     {'class': 'form-control', 'placeholder': 'username'})

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('dob', 'phone_number', 'country', 'address', 'postal_code', 'city', 'role', 'marketing')
        widgets = {
            'dob': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Select Role'})
        self.fields['dob'].widget.attrs.update(
            {'class': 'form-control datetimepicker-input', 'placeholder': 'Date of birth'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Phone number'})
        self.fields['country'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Country'})
        self.fields['address'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Address'})
        self.fields['postal_code'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Postal code'})
        self.fields['city'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'City'})
        self.fields['marketing'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Marketing'})


