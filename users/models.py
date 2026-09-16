from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    number_phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Payments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="дата оплаты")
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True)
    payment_amount = models.IntegerField(verbose_name="сумма оплаты")
    payment_method = models.IntegerField(verbose_name="способ оплаты")
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID сессии Stripe")
    link = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на оплату")
    product= models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:

         verbose_name = "платеж"
         verbose_name_plural = "платежи"




