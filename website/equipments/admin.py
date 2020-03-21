from django.contrib import admin

from .models import Camera, Lens, Accessories, Equipments

admin.site.site_header = "Padmashree Associates"
admin.site.site_title = "Padmashree Associates"
admin.site.index_title = 'Administrator Dashboard'

class EquipmentsInline(admin.StackedInline):
    model = Equipments
    fields = ['image']
    extra = 1

class CameraAdmin(admin.ModelAdmin):
    inlines = [EquipmentsInline, ]
    list_display = ['company', 'model']
    fields = ['company', 'model', 'description', 'inventory', 'ratings']

class LensAdmin(admin.ModelAdmin):
    inlines = [EquipmentsInline, ]
    list_display = ['company', 'model']
    fields = ['company', 'model', 'description', 'inventory', 'ratings']

class AccessoriesAdmin(admin.ModelAdmin):
    inlines = [EquipmentsInline, ]
    list_display = ['company', 'model']
    fields = ['company', 'model', 'description', 'inventory', 'ratings']

admin.site.register(Camera, CameraAdmin)
admin.site.register(Lens, LensAdmin)
admin.site.register(Accessories, AccessoriesAdmin)
