from django.contrib.auth.models import CustomUser, Zone, ZipZone, Plant, Slot, PlantZone, PlantSlot
from rest_framework import generics
from api.serializers import PlantSerializer, SlotSerializer, ZoneSerializer, CustomUserSerializer, PlantZoneSerializer, PlantSlotSerializer, PlantSlotActivity
from django.shortcuts import get_list_or_404, get_object_or_404


class ListAvailablePlants(generics.ListAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def get(self, request):
        #user = CustomUser.objects.get(id = user_id)
        user = get_object_or_404(CustomUser, id=self.request.user.pk)
        available_plants = user.zone.all_plants_in_a_zone()
        serializer = PlantZoneSerializer(available_plants)
        return Response(serializer.data)


class ListUserPlants(generics.ListAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        user_plants = 

