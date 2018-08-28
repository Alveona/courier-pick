from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Courier(models.Model):
    name = models.CharField(max_length=32, verbose_name="Имя курьера")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Аккаунт", null=True) # connecting courier with django user

    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = "Курьеры"

    def __str__(self):
        return 'Курьер %s' % (self.name)

class Order(models.Model):
    addressFrom = models.CharField(max_length=64, verbose_name="Адрес клиента")
    addressTo = models.CharField(max_length=64, verbose_name="Адрес доставки")
    price = models.IntegerField(null=True, verbose_name="Цена заказа")
    date = models.DateTimeField(default=timezone.now, verbose_name="Время заказа")
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, verbose_name="Курьер")

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"

    def __str__(self):
        return 'Заказ'

