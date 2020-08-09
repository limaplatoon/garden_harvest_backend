from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

User = get_user_model()

from api.models import Slot


@receiver(post_save, sender=User)
def create_slots(sender, instance, created, **kwargs):
    if created:
        slot_total = 4
        slots = [Slot(name=f'Slot {i+1}', user=instance)
                    for i in range(slot_total)]
        Slot.objects.bulk_create(slots)
