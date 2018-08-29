from rest_framework import serializers
from .models import Order, Courier
from . import maps
price_coeff = 120

class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ('name', )

class OrderSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True) # get courier parameters (here: name) by using serializer
    day = serializers.ReadOnlyField(source='getOrderDay') # using function to get date in dd/mm/yyyy

    def create(self, validated_data): # To set price and couriers when user creates orders
        distance_price_addition = maps.countDistanceFromAddresses(addressFrom=validated_data['addressFrom'], addressTo=validated_data['addressTo'])
        counted_price = int(validated_data['weight']) * distance_price_addition * price_coeff
        order = Order(addressTo = validated_data['addressTo'], addressFrom = validated_data['addressFrom'], weight = validated_data['weight'], price = counted_price)
        order.save()
        return order

    class Meta:
        model = Order
        fields = ('addressFrom', 'addressTo', 'weight', 'day', 'price', 'courier')