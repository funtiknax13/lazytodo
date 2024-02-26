from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.forms import UserLoginForm
from users.views import RegisterView, ProfileUpdateView, UserDetailView, confirm_email, generate_new_password, activate_email

app_name = UsersConfig.name

urlpatterns = [
    path('login', LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('register', RegisterView.as_view(), name='register'),
    path('profile/update', ProfileUpdateView.as_view(), name='update_profile'),
    path('profile', UserDetailView.as_view(), name='profile'),
    path('confirm', confirm_email, name='confirm'),
    path('activate<str:key>', activate_email, name='activate'),
    path('profile/genpassword', generate_new_password, name='genpassword')

]
