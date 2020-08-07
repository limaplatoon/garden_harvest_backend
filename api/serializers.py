from builtins import object
from rest_framework import serializers
from .models import Slot, Zone ,Plant ,PlantZone, PlantSlot

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

class SuggestedPlantSerializer(serializers.ModelSerializer):
    plant = PlantNameOnlySerializer()

    class Meta:
        model = PlantZone
        fields = [
            'plant',
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

