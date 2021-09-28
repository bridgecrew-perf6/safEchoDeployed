# from django.urls import reverse_lazy
# from django.views import generic
# from django.http import HttpResponse, HttpResponseRedirect
# from accounts.forms import WebSignUpForm
#
#
# class SignUp(generic.CreateView):
#     form_class = WebSignUpForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.save()
#         current_site = get_current_site(request)
#         subject = 'Activate Your MySite Account'
#         message = render_to_string('account_activation_email.html', {
#             'user': self.object,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': account_activation_token.make_token(user),
#         })
#         user.email_user(subject, message)
#         return HttpResponseRedirect(self.get_success_url())


from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView
from django.utils.encoding import force_text
from accounts.models import User
from .forms import SignupForm, ProfileForm
from django.urls import reverse
from django.conf import settings
from django.template import Template, Context
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.views import generic
from django.urls import reverse_lazy
from .tokens import account_activation_token


class SignUpView(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email_confirmation = False
            user.save()
            host = request.get_host()
            send_register_email(user, host)
            return redirect('signup_confirmation')
        return render(request, self.template_name, {'form': form})


class SignUpConfirmationView(View):
    template_name = 'signup_confirmation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class InvalidActivation(TemplateView):
    template_name = 'invaid_activation.html'


class SignUpActivationDone(TemplateView):
    template_name = 'signup_confirmation_done.html'


def send_register_email(user, host):
    try:
        subject, from_email, to = 'Email Confirmation', settings.EMAIL_HOST_USER, [user.email]
        html = render_to_string('signup_confirmation_email.html',
                                {
                                    'user': user,
                                    'domain': host,
                                    'uid': urlsafe_base64_encode(force_bytes(user.email)),
                                    'token': account_activation_token.make_token(user)
                                })
        content = Template(html).render(Context({}))
        msg = EmailMultiAlternatives(subject, content, from_email, to)
        msg.attach_alternative(content, "text/html")
        msg.send()
    except Exception as e:
        pass


def activate(request, uidb64, token):
    try:
        u_email = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=u_email)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('signup_activation_done')
    else:
        return redirect(reverse('invalid_activate'))


class ProfileCreateView(generic.CreateView):
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'profile_completion.html'
