from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import Q

from equipments.models import Equipment
from bookings.models import Event


@receiver(post_save, sender=Event)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        order = sender.objects.filter(start_day__exact=instance.start_day, 
                equipment_key=instance.equipment_key.pk).exclude(pk__exact=instance.pk)
        print(order)
        if order:
            latest_order = order.latest('pk')
            # print(latest_order)
            count = latest_order.inventory-1
            # print('here',count)
            instance.inventory = count
            instance.save()
        else:
            item = Equipment.objects.get(pk=instance.equipment_key.pk)
            count = item.count - 1
            # print('no this',count)
            instance.inventory = count
            instance.save()