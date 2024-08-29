from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering = ['dni']
    list_display = ('dni', 'first_name', 'last_name', 'email', 'numer_phone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('dni', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'email', 'numer_phone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('dni', 'email', 'first_name', 'last_name', 'numer_phone', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('dni', 'email', 'first_name', 'last_name')
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
 