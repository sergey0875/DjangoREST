from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from materials.models import Course, Subscriptions
from users.models import CustomUser


@shared_task
def email_notification(course_id):

    """Отправка сообщения об обновлении курса подписчикам"""

    course = Course.objects.get(pk=course_id)

    recipient_list = list(
        Subscriptions.objects.filter(course=course).values_list('user__email', flat=True)
    )

    # Если подписчиков нет, завершаем задачу без отправки писем
    if not recipient_list:
        return f"У курса '{course.name}' нет подписчиков."

    send_mail(f"Обновление курса: {course.name}", f"Курс '{course.name}' изменился, добавлены новые материалы.", EMAIL_HOST_USER, recipient_list)


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
