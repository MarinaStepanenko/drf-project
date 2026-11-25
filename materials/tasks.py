from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def send_information_about_subscription(email):
    send_mail(
        "Обновление курса!",
        "В курсе, на который вы подписаны, произошли изменения.",
        "noreply@mysite.com",
        [email],
    )


@shared_task
def deactivate_inactive_users():
    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago, last_login__isnull=False, is_active=True
    )

    inactive_users.update(is_active=False)
