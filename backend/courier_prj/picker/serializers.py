from rest_framework import serializers
from .models import Order, Courier
from . import maps
price_coeff = 120

class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ('name', ) # We return only name of courier to frontend when it POST on /api/orders/


MAX_COURIER_ORDERS_NUMBER = 3 # Maximum amount of orders courier can deliver in single date

class OrderSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(read_only=True) # get courier parameters (here: name) by using serializer
    day = serializers.ReadOnlyField(source='getOrderDay') # using function to get date in dd/mm/yyyy

    def create(self, validated_data):
        # set price and couriers when user creates orders
        distance_price_addition = maps.countDistanceFromAddresses(addressFrom=validated_data['addressFrom'], addressTo=validated_data['addressTo'])
        counted_price = int(validated_data['weight']) * distance_price_addition * price_coeff

        courier = Courier.objects.order_by('current_orders_number').first() # get courier with least orders number
        if courier.current_orders_number < 3:
            courier.current_orders_number = courier.current_orders_number + 1
            courier.save() # increasing courier's orders number
            order = Order(addressTo = validated_data['addressTo'], addressFrom = validated_data['addressFrom'], courier = courier, weight = validated_data['weight'], price = counted_price)
            order.save()
            return order
        raise serializers.ValidationError("На эту дату свободных курьеров нет")

    class Meta:
        model = Order
        fields = ('addressFrom', 'addressTo', 'weight', 'day', 'price', 'courier')