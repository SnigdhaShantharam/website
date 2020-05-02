from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import Q

from equipments.models import Equipment
from bookings.models import Event


@receiver(post_save, sender=Event)
def update_inventory(sender, instance, created, **kwargs):
    if created:
        # Profile.objects.create(user=instance)
        print(instance.pk)
        print(kwargs)
        order = sender.objects.filter(start_day__exact=instance.start_day, 
                equipment_key=instance.equipment_key.pk).exclude(pk__exact=instance.pk)
        print(order)
        if order:
            latest_order = order.latest('pk')
            print(latest_order)
            count = latest_order.inventory-1
            print('here',count)
            instance.inventory = count
            instance.save()
        else:
            item = Equipment.objects.get(pk=instance.equipment_key.pk)
            count = item.count - 1
            print('no this',count)
            instance.inventory = count
            instance.save()


# @receiver(pre_save, sender=Event)
# def update_inventory(sender, instance, **kwargs):
# #     # order = Event.objects.filter(
# #     #         Q(start_day__exact=instance.start_day)|Q(start_day__exact=instance.end_day)
# #     #     ).latest('pk')
# #     if instance:
# #         print(instance.pk)
# #         print(kwargs)
    # order = sender.objects.filter(start_day__exact=instance.start_day, 
    #             equipment_key=instance.equipment_key.pk).order_by('-pk').first()
    # if order:
    #     print(order)
    #     count = order.inventory-1
    #     print(count)
    #     instance.inventory = count
    #     instance.save()
    # else:
    #     item = Equipment.objects.get(pk=instance.equipment_key.pk)
    #     count = item.count - 1
    #     print(count)
    #     instance.inventory = count
    #     instance.save()

        
    # if order:
    #     print('order.inventory = ',order.inventory)
    #     instance.inventory = order.inventory - 1
    #     print('instance.inventory = ',instance.inventory)
    #     # instance.save(self.inventory=order.inventory - 1)
    # else:
        # item = Equipment.objects.get(pk=instance.equipment_key.pk).first()
        # print(item)
        # instance.inventory = item.count - 1
        # print('instance.inventory = ',instance.inventory)
        # instance.save()

# @receiver(pre_save, sender=Event)
# def updating(sender, instance, **kwargs):
#     if sender.objects.filter(start_day__exact=instance.start_day, 
#                 equipment_key=instance.equipment_key.pk).order_by('-pk').first():
#         order = sender.objects.filter(start_day__exact=instance.start_day, 
#                 equipment_key=instance.equipment_key.pk).order_by('-pk').first()
#         print(order)
#         count = order.inventory-1
#         print(count)
#         instance.inventory = count
#         instance.save()
    