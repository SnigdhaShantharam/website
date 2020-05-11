from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator 
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from website.settings import AUTH_USER_MODEL
from equipments.models import Equipment

booking_type = (
    (1, 'Online Booking'),
    (2, 'Offline Booking')
)

class Event(models.Model):
    customer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_type = models.IntegerField(choices=booking_type)
    equipment_key = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    start_day = models.DateField()
    start_time = models.TimeField()
    end_day = models.DateField()
    end_time = models.TimeField()
    inventory = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(0)])
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    advance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = u'Event'
        verbose_name_plural = u'Events'

    def __str__(self):
        return '{} - {}'.format(self.customer.first_name, self.equipment_key)

    def check_availability(self, fixed_startday, fixed_starttime, fixed_endday, fixed_endtime, new_startday, new_starttime, new_endday, new_endtime, inventory):
        availability = True
        if new_startday == fixed_endday or new_endday == fixed_startday:  # edge case
            print("1")
            new_starttime = new_starttime.hour*60 + new_starttime.minute
            new_endtime = new_endtime.hour*60 + new_endtime.minute
            fixed_starttime = fixed_starttime.hour*60 + fixed_starttime.minute
            fixed_endtime = fixed_endtime.hour*60 + fixed_endtime.minute

            if (new_starttime - fixed_endtime)/60 >= 3.0:
                print("1--1")
                if inventory == 0:
                    print("1--1-->1")
                    availability = False
                elif inventory is None:
                    print("1--1-->2")
                    availability = True
                elif inventory > 0:
                    availability = True
                    print("1--1-->3")
                    inventory -= 1
            elif (fixed_starttime - new_endtime)/60 >= 3.0:
                print("1--2")
                if inventory == 0:
                    print("1--2-->1")
                    availability = False
                elif inventory is None:
                    print("1--2-->2")
                    availability = True
                elif inventory > 0:
                    availability = True
                    print("1--2-->3")
                    inventory -= 1
            else:
                availability = False
                print("1--3")
        elif (new_startday >= fixed_startday and new_startday <= fixed_endday) or (new_endday >= fixed_startday and new_endday <= fixed_endday):  # innner limits
            # overlap = True
            print("2")
            if inventory == 0:
                print("2--1")
                availability = False
            elif inventory is None:
                print("2--2")
                availability = True
            elif inventory > 0:
                availability = True
                print("2--3")
                inventory -= 1
        elif new_startday <= fixed_startday and new_endday >= fixed_endday:  # outter limits
            # overlap = True
            print("3")
            if inventory == 0:
                availability = False
                print("3--1")
            elif inventory is None:
                availability = True
                print("3--2")
            elif inventory > 0:
                availability = True
                inventory -= 1
                print("3--3")

        return availability

    def get_absolute_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    def clean(self):
        if self.end_day < self.start_day:
            raise ValidationError('Please check the starting and ending dates')
        # event = Event.objects.filter(start_day=self.start_day).order_by('-id')[0]
        # events = Event.objects.filter(start_day=self.start_day).order_by('-id')
        events = Event.objects.filter(
            Q(start_day__exact=self.start_day, equipment_key=self.equipment_key)|
            Q(start_day__exact=self.end_day, equipment_key=self.equipment_key)
        ).order_by('-id')
        if events:
            for event in events:
                availability= self.check_availability(event.start_day, event.start_time, event.end_day, event.end_time, self.start_day, self.start_time, self.end_day, self.end_time, event.inventory)
                print(availability)
                if not availability:
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.start_day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))

