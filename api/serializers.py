from builtins import object
from rest_framework import serializers
from .models import Slot, Zone, Plant, PlantZone, PlantSlot
from api.utils.seed_planner import schedule, schedule_by_slot


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['pk', 'common_name', 'companions',
                  'description', 'harvest_max', 'harvest_min',
                  'scientific_name', 'sowing', 'spacing'
                  ]


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['pk', 'color', 'location_description',
                  'name', 'user'
                  ]


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['min_temp', 'zone']


class PlantZoneSerializer(serializers.ModelSerializer):
    plant = PlantSerializer()
    zone = ZoneSerializer()

    class Meta:
        model = PlantZone
        fields = ['pk', 'calendar', 'plant', 'zone']


class PlantSlotSerializer(serializers.ModelSerializer):
    plant_zone = PlantZoneSerializer()
    slot = SlotSerializer()

    class Meta:
        model = PlantSlot
        fields = ['pk', 'created_at', 'date_harvested',
                  'date_planted', 'date_seeded',
                  'harvest_date_max', 'harvest_date_min',
                  'plant_zone', 'slot'
                  ]


class CalendarSerializer(serializers.ModelSerializer):
    plant_zone = PlantZoneSerializer()
    slot = SlotSerializer()
    planned_duration = serializers.SerializerMethodField()
    requires_seeding = serializers.SerializerMethodField()

    def get_planned_duration(self, instance):
        harvest_max = instance.plant_zone.plant.harvest_max
        calendar = instance.plant_zone.calendar
        return (harvest_max + (56 if 'S' in calendar else 14))

    def get_requires_seeding(self, instance):
        return ('S' in instance.plant_zone.calendar)

    class Meta:
        model = PlantSlot
        fields = ['pk', 'created_at', 'date_planted',
                  'date_seeded', 'harvest_date_max',
                  'harvest_date_min', 'planned_duration',
                  'plant_zone', 'requires_seeding', 'slot'
                  ]


class AaronsSuperSerializer(serializers.ModelSerializer):
    pk = serializers.SerializerMethodField()
    plant = serializers.SerializerMethodField()
    plant_slot_id = serializers.SerializerMethodField()

    def get_pk(self, instance):
        return instance.plant_zone.id

    def get_plant(self, instance):
        return PlantSerializer(instance=instance.plant_zone.plant, many=False).data

    def get_plant_slot_id(self, instance):
        return instance.id

    class Meta:
        model = PlantSlot
        fields = ['pk', 'plant', 'plant_slot_id']


class ScheduleSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    plant = serializers.SerializerMethodField()

    def get_options(self, instance):
        return schedule(instance.plant_zone, instance.slot.user.id)

    def get_plant(self, instance):
        return PlantSerializer(instance.plant_zone.plant, many=False).data

    class Meta:
        model = PlantSlot
        fields = ['id', 'plant', 'options']


class SlotOptionsSerializer(serializers.ModelSerializer):
    earliest_date = serializers.SerializerMethodField()

    def get_earliest_date(self, instance):
        plant_zone = self.context.get('plant_zone')
        return schedule_by_slot(instance, plant_zone)
    
    class Meta:
        model = Slot
        fields = ['id', 'name', 'location_description', 'earliest_date']
