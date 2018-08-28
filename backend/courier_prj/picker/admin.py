from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Courier, Order


admin.site.register(Courier)
admin.site.register(Order)


