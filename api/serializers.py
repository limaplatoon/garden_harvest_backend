from builtins import object
from rest_framework import serializers
from .models import CustomUser, Slot, Zone ,Plant ,Plant_Zone, Plant_slot, PlantSlotActivity

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
            'name',
            'min_temp'
        ]

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'zip_code',
            'zone'
        ]

class Plant_ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant_Zone
        fields = [
            'plant',    
            'zone',
            'january',
            'february',
            'march',
            'april',
            'may',
            'june',
            'july',
            'august',
            'september',
            'october',
            'november',
            'december'
        ]

class Plant_slotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant_slot
        fields = [
            'plant_zone',
            'slot',
            'date_planted',
            'harvest_date_min',
            'harvest_date_max'
        ]

class PlantSlotActivity(serializers.ModelSerializer):
    class Meta:
        model = PlantSlotActivity
        fields = [
            'plant_slot',
            'activity'
        ]