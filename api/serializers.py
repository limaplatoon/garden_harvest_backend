from builtins import object
from rest_framework import serializers
from .models import CustomUser, Slot, Zone ,Plant ,PlantZone, PlantSlot, PlantSlotActivity

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = [
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

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'zip_code',
            'zone'
        ]

class PlantZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantZone
        fields = [
            'plant',    
            'zone',
            'calendar',
        ]

class PlantSlotSerializer(serializers.ModelSerializer):
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

