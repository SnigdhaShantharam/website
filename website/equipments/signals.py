from django.db.models.signals import post_save
from django.dispatch import receiver

from equipments.models import Equipment
from bookings.models import Event

