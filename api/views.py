from .models import Zone, Plant, Slot, PlantZone, PlantSlot
from rest_framework import generics
from rest_framework.response import Response
from api import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from api.utils.queries import retrieve_a_users_plants

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
    serializer_class = serializers.PlantSerializer


class UserPlants(generics.ListCreateAPIView):
    serializer_class = serializers.FilteredPlantSerializer

    def get(self, request):
        # This will change once auth login is completed
        user = User.objects.get(pk=4)
        plants = [plant_slot.plant_zone 
                  for plant_slot in PlantSlot.objects.filter(slot__user=user)]
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)


class Calendar(generics.ListAPIView):
    queryset = PlantSlot.objects.all()
    serializer_class = serializers.CalendarSerializer

    def get(self, request):
        # This will change once auth login is completed
        user = get_object_or_404(User, pk=1)
        events = list(retrieve_a_users_plants(user.id))
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


# class AddPlantToGarden(generics.ListCreateAPIView):
#     queryset = Plant.objects.all()
#     serializer_class = serializers.FilteredPlantSerializer

#     def post(self, request):
#         user = User.objects.get(pk=3)
