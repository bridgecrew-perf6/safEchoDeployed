from django.urls import path
from django.contrib.auth import views
from accounts import views as accountView

urlpatterns = [
    path('signup/', accountView.SignUpView.as_view(), name='signup'),
    path('signup_confirmation/', accountView.SignUpConfirmationView.as_view(), name='signup_confirmation'),
    path('activate/<str:uidb64>/<str:token>/', accountView.activate, name='activate'),
    path('invalid_activate/', accountView.InvalidActivation.as_view(), name='invalid_activate'),
    path('signup_activation_done/', accountView.SignUpActivationDone.as_view(), name='signup_activation_done'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('profile/create/', accountView.ProfileCreateView.as_view(), name='profile_completion')


]
