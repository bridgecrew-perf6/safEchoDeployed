from django.urls import reverse_lazy
from django.views import generic

from accounts.forms import WebSignUpForm


class SignUp(generic.CreateView):
    form_class = WebSignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
