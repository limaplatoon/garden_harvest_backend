import os
import json
from django.conf import settings
from django.db import migrations


DATA_PATH = os.path.join(settings.BASE_DIR, 'api', 'data')

def seed_zone_data(apps):
    print('\033[36m   - begin seed of hardiness zones \033[m')

    Zone = apps.get_model('api', 'Zone')

    filepath = os.path.join(DATA_PATH, 'hardiness_zones.json')
    with open(filepath, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        zones = []
        for zone, temp in data.items():
            zones.append(Zone(zone=zone, min_temp=temp))
    Zone.objects.bulk_create(zones)
    print('\033[32m   \u2713 hardiness zones data complete \033[m')


def seed_zipzone_data(apps):
    print("\033[36m   - begin seed of zipzones \033[m")
    
    ZipZone = apps.get_model('users', 'ZipZone')

    filepath = os.path.join(DATA_PATH, 'zip_zones.json')
    with open(filepath, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file) # 41,120 zip zones.
        zipzones = []
        for zipcode, zone in data.items():
            if len(zipzones) < 750:
                zipzones.append(ZipZone(zip_code=zipcode, zone=zone))
            else:
                zipzones.append(ZipZone(zip_code=zipcode, zone=zone))
                ZipZone.objects.bulk_create(zipzones)
                zipzones = []
        ZipZone.objects.bulk_create(zipzones)
    print("\033[32m   \u2713 zipzones data complete \033[m")


def seed_plantzone_data(apps, plant_obj, calendars):
    PlantZone = apps.get_model('api', 'PlantZone')
    Zone = apps.get_model('api', 'Zone')
    plantzones = []
    for zone_key, calendar in calendars.items():
        zone = Zone.objects.get(zone=zone_key)
        calendar_str = ','.join(calendar.values())
        pzone = PlantZone(plant=plant_obj,
                          zone=zone,
                          calendar=calendar_str)
        plantzones.append(pzone)
    PlantZone.objects.bulk_create(plantzones)


def seed_plant_and_plantzone_data(apps):
    print("\033[36m   - begin seed of plant and plantzone data \033[m")
    print("\033[31m    ( May take up to 20s to complete ) \033[m")
    
    Plant = apps.get_model('api', 'Plant')

    filepath = os.path.join(DATA_PATH, 'all_data.json')
    with open(filepath, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for item in data:
            harvest = item.pop('harvest')
            zcalendars = item.pop('zone_calendars')
            item.update({'harvest_min': harvest.get('from'),
            'harvest_max': harvest.get('to')})
            plant = Plant.objects.create(**item)
            # build plantzones while building plants.
            seed_plantzone_data(apps, plant, zcalendars)
    print("\033[32m   \u2713 plant and plantzone data complete \033[m")


def seed_all_data(apps, schema_editor):
    print("\033[1;37m - begin seeding database \033[m")
    seed_zone_data(apps)
    seed_zipzone_data(apps)
    seed_plant_and_plantzone_data(apps)
    print("\033[1;33m \u2713 database seeding complete \033[m")


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            seed_all_data,
            reverse_code=migrations.RunPython.noop),
    ]