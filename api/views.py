from .models import Zone, Plant, Slot, PlantZone, PlantSlot
from rest_framework import generics
from rest_framework.response import Response
from api import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class ListAvailablePlants(generics.ListAPIView):
    queryset = PlantZone.objects.all()
    serializer_class = serializers.FilteredPlantSerializer

    def get(self, request):
        # This will change once auth login is completed
        user = User.objects.get(pk=1)
        plant_zones = user.zone.plants.exclude(calendar__contains=','*11)
        serializer = self.get_serializer(plant_zones, many=True)
        return Response(serializer.data)


class PlantDetail(generics.RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = serializers.PlantSlotSerializer


class UserPlants(generics.ListAPIView):
    serializer_class = serializers.FilteredPlantSerializer

    def get(self, request):
        # This will change once auth login is completed
        user = User.objects.get(pk=3)
        plants = [plant_slot.plant_zone 
                  for plant_slot in PlantSlot.objects.filter(slot__user=user)]
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)
        