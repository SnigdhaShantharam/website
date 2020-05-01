from django.contrib import admin

from .models import Event

class BookingsAdmin(admin.ModelAdmin):
    list_display = ['customer', 'equipment_key', 'start_day', 'end_day', 'booking_type']

admin.site.register(Event, BookingsAdmin)
# admin.site.register(Event)