from .models import Zone, Plant, Slot, PlantZone, PlantSlot
from api import serializers
from api.utils.seed_planner import schedule
from api.utils.queries import retrieve_a_users_plants,plants_that_can_be_seeded_this_month, plants_that_can_be_planted_this_month,current_status_of_all_user_plants, all_plants_that_could_be_grown_in_this_zone
from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseNotAllowed
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json


User = get_user_model()

class ListAvailablePlants(generics.ListAPIView):
    queryset = PlantZone.objects.all()
    serializer_class = serializers.PlantZoneSerializer

    def get(self, request):
        # This will change once auth login is completed
        user = User.objects.get(pk=request.user.pk)
        plant_zones = user.zone.plants.exclude(calendar__contains=','*11)
        serializer = self.get_serializer(plant_zones, many=True)
        return Response(serializer.data)


class PlantDetail(generics.RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = serializers.PlantSerializer


class UserPlants(generics.ListCreateAPIView):
    queryset = PlantSlot.objects.all()
    serializer_class = serializers.PlantZoneSerializer

    def get(self, request):
        # This will change once auth login is completed
        user = User.objects.get(pk=request.user.pk)
        plants = [plant_slot.plant_zone 
                  for plant_slot in PlantSlot.objects.filter(slot__user=user)]
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)


class Calendar(generics.ListAPIView):
    queryset = PlantSlot.objects.all()
    serializer_class = serializers.CalendarSerializer

    def get(self, request):
        # This will change once auth login is completed
        user = get_object_or_404(User, pk=request.user.pk)
        events = list(retrieve_a_users_plants(user.id).filter(date_harvested__isnull=True))
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
@csrf_exempt
def AddPlant(request, plant_zone_id):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        plant_zone = get_object_or_404(PlantZone, pk=plant_zone_id)
        new_slot = user.slots.first()
        new_plant_slot = PlantSlot.objects.create(plant_zone=plant_zone, slot=new_slot)
        serialized_plant_slot = serializers.AaronsSuperSerializer(new_plant_slot, many=False).data
        return JsonResponse(data=serialized_plant_slot, status=201)
    return HttpResponseNotAllowed(['POST'])


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
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
        serialized_data = serializers.CalendarSerializer(event, many=False).data
        return Response(serialized_data)
    return HttpResponseNotAllowed(['POST'])


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
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
        serialized_data = serializers.CalendarSerializer(event, many=False).data
        return Response(serialized_data)
    return HttpResponseNotAllowed(['POST'])


@api_view(('POST',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
@csrf_exempt
def DeletePlant(request,plant_slot_id):
    if request.method == 'POST':
        event = get_object_or_404(PlantSlot, pk=plant_slot_id)
        event.delete()
        return JsonResponse(data={'status':'success'}, status=200)
    return HttpResponseNotAllowed(['POST'])

class DetermineSchedule(generics.RetrieveAPIView):
    queryset = PlantSlot.objects.all()
    serializer_class = serializers.ScheduleSerializer

@api_view(('GET',))
@renderer_classes((JSONRenderer, TemplateHTMLRenderer))
def plant_something_new_this_month(request):
    #edit next line once user auth is implemented
    user = get_object_or_404(User, pk=request.user.pk)
    zone = get_object_or_404(Zone, users__id=user.id)
    can_be_seeded = plants_that_can_be_seeded_this_month(user.id, zone)
    can_be_planted = plants_that_can_be_planted_this_month(user.id, zone)
    serial_seeded = serializers.PlantZoneSerializer(can_be_seeded, many=True).data
    serial_planted = serializers.PlantZoneSerializer(can_be_planted, many=True).data
    something_new_this_month = {'can_be_seeded':serial_seeded, 'can_be_planted':serial_planted}
    return Response(something_new_this_month)

class PlantSlotStatus(generics.ListAPIView):
    queryset = PlantSlot.objects.all()
    serializer_class = serializers.PlantSlotSerializer

    def get(self, request):
        # This will change once auth login is completed
        user = get_object_or_404(User, pk=request.user.pk)
        to_be_scheduled, to_be_seeded, to_be_transplanted, to_be_planted, to_be_harvested, harvested_plants = current_status_of_all_user_plants(user.id)
        scheduled = self.get_serializer(to_be_scheduled, many=True).data
        seeded = self.get_serializer(to_be_seeded, many=True).data
        transplanted = self.get_serializer(to_be_transplanted, many=True).data
        planted = self.get_serializer(to_be_planted, many=True).data
        harvested = self.get_serializer(to_be_harvested, many=True).data
        history = self.get_serializer(harvested_plants, many=True).data
        result = {'to_be_scheduled': scheduled, 'to_be_seeded': seeded, 'to_be_transplanted': transplanted, 'to_be_planted': planted, 'to_be_harvested': harvested, 'harvested_plants': history}
        return Response(result)

class WhatCanBeGrownInMyArea(generics.ListAPIView):
    queryset = PlantZone.objects.all()
    serializer_class = serializers.PlantZoneSerializer

    def get(self, request):
        # This will change once auth login is completed
        user = get_object_or_404(User, pk=request.user.pk)
        zone = get_object_or_404(Zone, users__id=user.id)
        possible_plants = all_plants_that_could_be_grown_in_this_zone(zone)
        serialized_list = self.get_serializer(possible_plants, many=True).data
        return Response(serialized_list)
