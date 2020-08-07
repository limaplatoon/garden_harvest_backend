from .models import Zone, ZipZone, Plant, Slot, PlantZone, PlantSlot
from rest_framework import generics
from django.http import HttpResponse
from api.serializers import PlantSerializer, SlotSerializer, ZoneSerializer, ZipZoneSerializer, PlantZoneSerializer, PlantSlotSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

def plants_by_zone(zone):
    return Zone.objects.get(zone = zone).plants.all()

class ListAvailablePlants(generics.ListAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def get(self, request):
        user = User.objects.get(pk=2)
        user.zip_code = "60603"
        user.zone = "6a"
        plant_zones = plants_by_zone(user.zone)
        serializer = PlantZoneSerializer(plant_zones, many=True)
        return HttpResponse(serializer.data)

    # def get(self, request):
    #     #user = CustomUser.objects.get(id = user_id)
    #     user = get_object_or_404(CustomUser, id=self.request.user.pk)
    #     available_plants = user.zone.all_plants_in_a_zone()
    #     serializer = PlantZoneSerializer(available_plants)
    #     return HttpResponse(serializer.data)


# class ListUserPlants(generics.ListAPIView):
#     queryset = Plant.objects.all()
#     serializer_class = PlantSerializer


# Create your views here.
