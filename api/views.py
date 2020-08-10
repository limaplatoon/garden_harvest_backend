from .serializers import CalendarSerializer
from .models import Zone, Plant, Slot, PlantZone, PlantSlot
from rest_framework import generics
from rest_framework.response import Response
from api import serializers
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from api.utils.queries import retrieve_a_users_plants
from api.utils.seed_planner import schedule
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json


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
    queryset = PlantSlot.objects.all()
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


@csrf_exempt
def AddPlant(request, user_id, plant_zone_id):  #item_create
    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)
        plant_zone = get_object_or_404(PlantZone, pk=plant_zone_id)
        new_slot = user.slots.first()
        new_plant_slot = PlantSlot.objects.create(plant_zone=plant_zone, slot=new_slot)
        serialized_plant_slot = serializers.AaronsSuperSerializer(new_plant_slot, many=False).data
        return JsonResponse(data=serialized_plant_slot, status=201)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def book_this_plant(request, plant_slot_id):
    if request.method == 'POST':
        event = get_object_or_404(PlantSlot,pk=plant_slot_id)
        date = json.loads(request.POST)
        #remove below when front end is working
        date.accepted_date = timezone.now()
        #remove above line when front end is working
        event.created_at = date.accepted_date
        event.save()
        serialized_data = CalendarSerializer(event, many=False).data
        return Response(serialized_data)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def UpdatePlant(request,plant_slot_id):
    if request.method == 'POST':
        event = get_object_or_404(PlantSlot, pk=plant_slot_id)
        requires_seeding = ( 'S' in event.plant_zone.calendar )
        if requires_seeding and not event.date_seeded:
            event.date_seeded = timezone.now()
        elif not event.date_planted:
            event.date_planted = timezone.now()
            min_date = (timezone.timedelta(days=(event.plant_zone.plant.harvest_min )))
            max_date = (timezone.timedelta(days=(event.plant_zone.plant.harvest_max)))
            event.harvest_date_min = event.date_planted + min_date
            event.harvest_date_max = event.date_planted + max_date
        else:
            event.date_harvested = timezone.now()
        event.save()
        serialized_data = CalendarSerializer(event, many=False).data
        return Response(serialized_data)
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def DeletePlant(request,plant_slot_id):
    if request.method == 'POST':
        event = get_object_or_404(PlantSlot, pk=plant_slot_id)
        event.delete()
        return JsonResponse(data={'status':'success'}, status=200)
    return HttpResponseNotAllowed(['POST'])

class DetermineSchedule(generics.RetrieveAPIView):
    queryset = PlantSlot.objects.all()
    serializer_class = serializers.MakeANewSerializer








'''
def determine_possible_schedule(request, plant_slot_id):
    plant_slot_object = get_object_or_404(PlantSlot, pk=plant_slot_id)
    possible_options = schedule(plant_slot_object.plant_zone, plant_slot_object.slot.user.id)
    final_result = (plant_slot_id, possible_options)
    serialized_data = MakeANewSerializer(final_result)
    return JsonResponse(data=serialized_data, status=200)
#retrieve plantSlot_Id abbreviated as PS from request
        #call seedplaner with (PS.plant_zone, PS.slot.user.id)
        #recieve sorted list by earliest planting time [(date, slot_object)] from above call to seedplaner
        #return options as follows (current plant_slot_id, sorted_list)
'''