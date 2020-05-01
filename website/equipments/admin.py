from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Equipment
# Camera, Lens, Accessories, Equipment_Images, 

admin.site.site_header = "Padmashree Associates"
admin.site.site_title = "Padmashree Associates"
admin.site.index_title = 'Administrator Dashboard'

# class ImagesInline(admin.StackedInline):
#     model = Equipment_Images
#     fields = ['image']
#     extra = 1

class EquipmentsAdmin(admin.ModelAdmin):
    # inlines = [ImagesInline, ]
    readonly_fields = ('slug',)
    list_display = ['equipment_type', 'company', 'model_name', 'count']
    fields = ['equipment_type', 'company', 'model_name', 'image', 'description', 'count', 'ratings', 'cost','slug']

admin.site.register(Equipment, EquipmentsAdmin)
# admin.site.register(Equipment_Images)

admin.site.unregister(Group)