from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from accounts.models import User


class LoginSuperUserRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_superuser:
            return HttpResponse('<h1>Permission is not allowed</h1>')
        return super().dispatch(request, *args, **kwargs)
