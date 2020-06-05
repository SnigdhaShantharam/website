from django.contrib import admin
import datetime
import calendar
from django.urls import reverse
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe

from .utils import EventCalendar
from .models import Event, EnquiryItem, EnquiryCart

class BookingsAdmin(admin.ModelAdmin):

    list_display = ['customer', 'equipment_key', 'start_day', 'end_day', 'booking_type']
    list_per_page = 15
    # search_fields = ['customer', 'booking_type']
    change_list_template = 'admin/bookings/change_list.html'
 
    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}
        cal = EventCalendar()
        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()
 
        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month
 
        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month
 
        extra_context['previous_month'] = reverse('admin:bookings_event_changelist') + '?start_day__gte=' + str(previous_month)
        extra_context['next_month'] = reverse('admin:bookings_event_changelist') + '?startday__gte=' + str(next_month)
        # print(extra_context)
        # cal = HTMLCalendar()
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return super(BookingsAdmin, self).changelist_view(request, extra_context)
 

admin.site.register(Event, BookingsAdmin)
admin.site.register(EnquiryItem)
admin.site.register(EnquiryCart)