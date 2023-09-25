from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UserAppConfig
from users.views import RegisterView, ProfileView, email_confirm, PasswordResetView

app_name = UserAppConfig.name


urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('confirm-email/<str:email_confirm_key>', email_confirm, name='email_confirm'),
    path('profile/', ProfileView.as_view(), name='profile'),
]