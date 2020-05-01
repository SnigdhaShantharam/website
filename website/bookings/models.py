from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
# from django.contrib.auth.models import User

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
    inventory = models.IntegerField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    advance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = u'Event'
        verbose_name_plural = u'Events'

    def __str__(self):
        return '{} - {}'.format(self.customer.first_name, self.equipment_key)

    def save(self, *args, **kwargs):
        # if inventory is None:
        #     self.inventory = 0
        # self.inventory = inventory
        if self.inventory is None:
            self.inventory = (self.equipment_key.inventory - 1)
        # else:
        #     self.inventory = inventory
        super(Event, self).save(*args, **kwargs)

    def check_availability(self, fixed_startday, fixed_starttime, fixed_endday, fixed_endtime, new_startday, new_starttime, new_endday, new_endtime, inventory):
        # overlap = False
        availability = True
        if new_startday == fixed_endday or new_endday == fixed_startday:  # edge case

            new_starttime = new_starttime.hour*60 + new_starttime.minute
            new_endtime = new_endtime.hour*60 + new_endtime.minute
            fixed_starttime = fixed_starttime.hour*60 + fixed_starttime.minute
            fixed_endtime = fixed_endtime.hour*60 + fixed_endtime.minute

            if (new_starttime - fixed_endtime)/60 >= 3.0:
                availability = True
                inventory -= 1
                # setattr(self.inventory, value=self.inventory-1)
            elif (fixed_starttime - new_endtime)/60 >= 3.0:
                availability = True
                inventory -= 1
                # setattr(self.inventory, value=self.inventory-1)
            else:
                availability = False
        elif (new_startday >= fixed_startday and new_startday <= fixed_endday) or (new_endday >= fixed_startday and new_endday <= fixed_endday):  # innner limits
            # overlap = True
            if inventory == 0:
                availability = False
            elif inventory is None:
                availability = True
            elif inventory > 0:
                availability = True
                inventory -= 1
        elif new_startday <= fixed_startday and new_endday >= fixed_endday:  # outter limits
            # overlap = True
            if inventory == 0:
                availability = False
            elif inventory > 0:
                availability = True
                inventory -= 1

        return availability, inventory

    def get_absolute_url(self):
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(self.pk,))

    def clean(self):
        if self.end_day < self.start_day:
            raise ValidationError('Please check the starting and ending dates')

        event = Event.objects.filter(
            start_day=self.start_day).order_by('-id')[0]
        if event:
            availability, inventory = self.check_availability(
                event.start_day, event.start_time, event.end_day, event.end_time, self.start_day, self.start_time, self.end_day, self.end_time, event.inventory)
            if availability is True:
                self.save(inventory)
            else:
                raise ValidationError(
                    'There is an overlap with another event: ' + str(event.start_day) + ', ' + str(
                        event.start_time) + '-' + str(event.end_time))
        # events = Event.objects.filter(start_day=self.start_day).order_by('-id')[0]
        # if events:
        #     for event in events:
        #         availability, inventory = self.check_availability(event.start_day, event.start_time, event.end_day, event.end_time, self.start_day, self.start_time, self.end_day, self.end_time, event.inventory)
        #         if availability is True:
        #             self.save(inventory=inventory)
        #         else:
        #             raise ValidationError(
        #                 'There is an overlap with another event: ' + str(event.start_day) + ', ' + str(
        #                     event.start_time) + '-' + str(event.end_time))
        else:
            self.save((self.equipment_key.inventory-1))
            