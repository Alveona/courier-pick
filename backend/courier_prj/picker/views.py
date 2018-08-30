from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )
    http_method_names = ['get', 'post']

    def get_queryset(self):  # Return only current courier's orders or all orders if superuser in GET /api/orders/
        user = self.request.user
        if user.is_superuser:
            queryset = Order.objects.all()
            return queryset
        return Order.objects.all().filter(courier__user=user)
