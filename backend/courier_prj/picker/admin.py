from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Courier, Order
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class UserAdminAuthenticationForm(AuthenticationForm):
    """
            Using Django AdminAuthenticationForm to login couriers
    """
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("This account is inactive."),
               code='inactive',
            )
class UserAdmin(AdminSite):
    """
        Please never grant your couriers permission to use default django admin panel
    """
    login_form = UserAdminAuthenticationForm

    def has_permission(self, request):
        # As default django admin form checks for is_staff
        return request.user.is_active

class UserAdminModel(admin.ModelAdmin):
    def get_queryset(self, request): # function to display only current courier's orders in manage panel
        qs = super(UserAdminModel, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(courier__user=request.user) # courier__user is actually SQL JOIN of courier and user models



admin.site.register(Courier)
admin.site.register(Order)

user_admin_site = UserAdmin(name="usersadmin")
user_admin_site.register(Courier, UserAdminModel)
user_admin_site.register(Order, UserAdminModel)


