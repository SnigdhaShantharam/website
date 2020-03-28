from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django.contrib.gis.admin import OSMGeoAdmin

from users import models

class UserAdmin(BaseUserAdmin, OSMGeoAdmin):
    ordering = ['id']
    list_display = ['phone_number', 'first_name']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal Info'), 
            {'fields': 
                ('first_name', 'last_name', 'address', 'city', 'location')}
            ),
        (_('Proof'), 
            {'fields': 
                ('id_proof_number','image')}
            ),
        (
            _('Permissions'),
                {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )

admin.site.register(models.User, UserAdmin)
