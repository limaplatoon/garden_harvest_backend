from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Zone(models.Model):
    zone = models.CharField(max_length=3, primary_key=True)
    min_temp = models.IntegerField()

    def all_plants_in_a_zone(self):
        return list(self.plants.all())


class ZipZone(models.Model):
    zip_code = models.CharField(max_length=5, primary_key=True)
    zone = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return f'{self.zipcode} (zone {self.zone})'


class Plant(models.Model):
    common_name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    sowing = models.TextField()
    spacing = models.TextField()
    harvest_min = models.IntegerField(default=1)
    harvest_max = models.IntegerField(default=1)
    companions = models.TextField(default='')
    description = models.TextField()

    def __str__(self):
        return f'{self.common_name}'


class CustomUser(AbstractUser):
    zip_code = models.CharField(max_length=100, blank=False)
    zone = models.ForeignKey(Zone, related_name="users",
                             on_delete=models.CASCADE)


class Slot(models.Model):
    user = models.ForeignKey(
        CustomUser, related_name='slots', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='unnamed')
    color = models.CharField(max_length=100, default='#C0BD7C')
    location_description = models.CharField(max_length=100, default='')

    def when_can_I_harvest(self):
        plants = list(self.plant.all())
        harvest_ranges = []
        for plant in plants:
            harvest_min = plant.harvest_date_min
            harvest_max = plant.harvest_date_max
            plant_name = plant.plant_zone.plant.common_name
            harvest_ranges.append((plant_name, harvest_min, harvest_max))
        return harvest_ranges


class Plant_Zone(models.Model):
    plant = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name='zones')
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, related_name='plants')
    january = models.CharField(max_length=3, default='')
    february = models.CharField(max_length=3, default='')
    march = models.CharField(max_length=3, default='')
    april = models.CharField(max_length=3, default='')
    may = models.CharField(max_length=3, default='')
    june = models.CharField(max_length=3, default='')
    july = models.CharField(max_length=3, default='')
    august = models.CharField(max_length=3, default='')
    september = models.CharField(max_length=3, default='')
    october = models.CharField(max_length=3, default='')
    november = models.CharField(max_length=3, default='')
    december = models.CharField(max_length=3, default='')

    def __str__(self):
        return f"plant: {self.plant.name} - zone: {self.zone.name}"

    class Meta:
        unique_together = ['plant', 'zone']


class Plant_slot(models.Model):
    plant_zone = models.ForeignKey(
        Plant_Zone, on_delete=models.CASCADE, related_name="slots")
    slot = models.ForeignKey(
        Slot, on_delete=models.CASCADE, related_name="plant")
    date_seeded = models.DateField(blank=True, null=True, default=None)
    date_transplanted = models.DateField(blank=True, null=True, default=None)
    date_planted = models.DateField(blank=True, null=True)
    harvest_days_min = models.IntegerField(default=1)
    harvest_days_max = models.IntegerField(default=1)

    def __str__(self):
        return f"plant: {self.plant_zone.plant.name}-{self.slot.location_description}-{self.date_planted}"

    class Meta:
        unique_together = ['plant_zone', 'slot', 'date_planted']
