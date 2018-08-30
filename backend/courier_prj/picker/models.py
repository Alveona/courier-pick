from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save

# Signal to assign all couriers to group by default when courier created
# (i.e. grant them permissions to view their orders in api and manage panel)
def default_group(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='couriers'))

post_save.connect(default_group, sender=User)

class Courier(models.Model):
    name = models.CharField(max_length=32, verbose_name="Имя курьера")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Аккаунт", null=True) # connecting courier with django user
    """ 
        Extra field as it would be really slow to check it through Order table every single time
        Please note that it is not expected to create orders directly from admin panel
        In that case you will not have this value increased because it is increased in serializers.py 
        when order is created by user
    """
    current_orders_number = models.IntegerField(default=0, verbose_name="Текущее количество заказов")
    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = "Курьеры"

    def __str__(self):
        return 'Курьер %s' % (self.name)

class Order(models.Model):
    addressFrom = models.CharField(max_length=64, verbose_name="Адрес клиента")
    addressTo = models.CharField(max_length=64, verbose_name="Адрес доставки")
    weight = models.IntegerField(verbose_name="Вес товара", default=0)
    price = models.IntegerField(null=True, verbose_name="Цена заказа")
    date = models.DateTimeField(default=timezone.now, verbose_name="Время заказа")
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, verbose_name="Курьер")

    def getOrderDay(self):
        return self.date.date().strftime("%d/%m/%Y") # Function uses in serializer to show date in GET request

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = "Заказы"

    def __str__(self):
        return 'Заказ от %s' % (self.date.date())

