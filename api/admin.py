from django.contrib import admin
from .models import Slot, Zone ,Plant ,PlantZone, PlantSlot

# Register your models here.
admin.site.register(Zone)
admin.site.register(Plant)
admin.site.register(Slot)
admin.site.register(PlantZone)
admin.site.register(PlantSlot)