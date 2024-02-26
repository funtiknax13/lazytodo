import secrets
import string

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string


def generate_secret_key(length: int) -> str:
    alphabet = string.ascii_letters + string.digits
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key


def confirm_user_email(request, user):
    secret_key = generate_secret_key(30)
    user.email_confirm_key = secret_key
    user.save()

    current_site = get_current_site(request)
    message = render_to_string('users/confirm_email_message.html', {
        'domain': current_site.domain,
        'key': secret_key,
    })
    send_mail(
        subject='Подтверждение почты',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )
