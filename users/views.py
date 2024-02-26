from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from utils.utils import generate_secret_key, confirm_user_email


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        confirm_user_email(self.request, self.object)
        self.object.save()
        return super().form_valid(form)


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(DetailView):
    model = User

    def get_object(self, queryset=None):
        return self.request.user


def confirm_email(request):
    confirm_user_email(request, request.user)
    return redirect(reverse('users:profile'))


def activate_email(request, key):
    user = User.objects.filter(email_confirm_key=key).first()
    user.email_is_confirmed = True
    user.email_confirm_key = None
    user.save()
    return redirect('/')


def generate_new_password(request):
    new_password = generate_secret_key(12)
    request.user.set_password(new_password)
    request.user.save()
    send_mail(
        subject='Вы сменили пароль',
        message=f'Новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    return redirect(reverse('users:login'))
