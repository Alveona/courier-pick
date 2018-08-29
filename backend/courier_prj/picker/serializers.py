from rest_framework import serializers
from .models import Order, Courier


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ('name', )

class OrderSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True) # get courier parameters (here: name) by using serializer
    day = serializers.ReadOnlyField(source='getOrderDay') # using function to get date in dd/mm/yyyy

    class Meta:
        model = Order
        fields = ('addressFrom', 'addressTo', 'day', 'price', 'courier')