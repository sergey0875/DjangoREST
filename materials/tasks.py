from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from users.models import CustomUser


@shared_task
def add(email):

    """ Отправка сообщения на email"""

    send_mail('Новелла подписка', 'Изменения в новой подписке', EMAIL_HOST_USER, [email])


@shared_task
def block_inactive_users():

    """ Блокировка пользователей которые заходили больше месяца назад"""

    one_month_ago = timezone.now() - timedelta(days=30) # вычитаю 30 дней с текущей даты.
    inactive_users = CustomUser.objects.filter(
        is_active=True,
        last_login__lt=one_month_ago,
        last_login__isnull=False
    )

    updated_count = inactive_users.update(is_active=False) #обновляю флаг в базе данных

    # Возвращаю количество заблокированных пользователей.
    return f"Заблокировано пользователей: {updated_count}"
