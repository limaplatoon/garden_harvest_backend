from builtins import object
from rest_framework import serializers
from .models import Slot, Zone ,Plant ,PlantZone, PlantSlot
from api.utils.seed_planner import schedule

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = [
            'pk',
            'common_name',
            'scientific_name',
            'sowing',
            'spacing',
            'harvest_min',
            'harvest_max',
            'companions',
            'description'
        ]

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = [
            'user',
            'name',
            'color',
            'location_description'
        ]

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = [
            'zone',
            'min_temp'
        ]

class PlantNameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = [
            'pk',
            'common_name',
            "scientific_name"
        ]


class PlantZoneSerializer(serializers.ModelSerializer):
    
    plant = PlantNameOnlySerializer()

    class Meta:
        model = PlantZone
        fields = [
            'plant',    
            'zone',
            'calendar',
        ]

class FilteredPlantSerializer(serializers.ModelSerializer):
    plant = PlantNameOnlySerializer()

    class Meta:
        model = PlantZone
        fields = [
            'pk',
            'plant',
        ]

class PlantSlotSerializer(serializers.ModelSerializer):

    plant = PlantNameOnlySerializer()

    class Meta:
        model = PlantSlot
        fields = [
            'plant_zone',
            'slot',
            'date_seeded',
            'date_planted',
            'date_harvested',
            'harvest_date_min',
            'harvest_date_max',
        ]


class CalendarPlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ['id','common_name','harvest_max','harvest_min','sowing','spacing']


class CalendarSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = ['id', 'color','location_description','name']


class CalendarZoneSerializer(serializers.ModelSerializer):
    plant = CalendarPlantSerializer()

    class Meta:
        model = PlantZone
        fields = ['calendar', 'plant']


class CalendarSerializer(serializers.ModelSerializer):
    plant_zone = CalendarZoneSerializer()
    slot = CalendarSlotSerializer()
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
        fields = ['id','created_at', 'date_planted', 'date_seeded', 'harvest_date_max', 'harvest_date_min', 'planned_duration', 'plant_zone', 'requires_seeding', 'slot']



class AaronsSuperSerializer(serializers.ModelSerializer):
    pk = serializers.SerializerMethodField()
    plant = serializers.SerializerMethodField()
    plant_slot_id = serializers.SerializerMethodField()

    def get_pk(self, instance):
        return instance.plant_zone.id
    
    def get_plant(self, instance):
        return PlantNameOnlySerializer(instance=instance.plant_zone.plant, many=False).data
        
    def get_plant_slot_id(self, instance):
        return instance.id

    class Meta:
        model = PlantSlot
        fields = [
            'pk',
            'plant',
            'plant_slot_id'
        ]

class MakeANewSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    def get_options(self, instance):
        return schedule(instance.plant_zone, instance.slot.user.id)
    
    class Meta:
        model = PlantSlot
        fields = ['id', 'options']
