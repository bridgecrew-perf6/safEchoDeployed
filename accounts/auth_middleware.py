from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.models import Profile


class LoginProfileRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not Profile.objects.filter(user=request.user).exists():
            return HttpResponseRedirect(reverse('profile_completion'))
        return super().dispatch(request, *args, **kwargs)
