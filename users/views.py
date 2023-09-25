from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm, PasswordResetForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()
        new_user.email_confirm_key = get_random_string(length=50)
        new_user.save()
        link = settings.SITE_URL + reverse_lazy('users:email_confirm', kwargs={'email_confirm_key': new_user.email_confirm_key})
        send_mail(
            subject='Поздравляем с регистрацией',
            message=f'Вы зарегистрированы на сайте Интернет-магазина Skystore!'
                    f'Ваша ссылка для подтверждения почты: {link}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def email_confirm(request, email_confirm_key):
    user = get_object_or_404(User, email_confirmed=False, email_confirm_key=email_confirm_key)

    user.email_confirmed = True
    user.save()

    return HttpResponse('Ваша почта подтверждена')


class PasswordResetView(View):

    def get(self, request):

        context = {
            'form': PasswordResetForm()
        }

        return render(template_name='users/password_reset.html', request=request, context=context)

    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.get(email=email)

        new_password = get_random_string(length=10)
        user.set_password(new_password)
        user.save()

        send_mail(
            subject='Изменение пароля',
            message=f'Ваш пароль успешно изменен. Новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        return HttpResponse('Вам на почту выслан новый пароль')
