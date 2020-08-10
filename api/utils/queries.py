from django.utils import timezone
from api.models import PlantSlot

#all queries will return a queryset object that can be converted to a list of objects by list(results)

# get all plant-slots that a user is keeping track of can also be filtered by anything unique to the user such as email or username
def retrieve_a_users_plants(user_id):
    return PlantSlot.objects.filter(slot__user__id=user_id)

#get plants/slots that need to be seeded
def plants_to_be_seeded(user_id):
    plants = retrieve_a_users_plants(user_id).filter(plant_zone__calendar__icontains='S')
    return [plant for plant in plants if not plant.date_seeded]

#get plants/slots that need to be transplanted
def plants_to_be_transplanted(user_id):
    plants = retrieve_a_users_plants(user_id).filter(plant_zone__calendar__icontains='S')
    return [plant for plant in plants if plant.date_seeded and not plant.date_planted]

#get plants/slots that need to be planted
def plants_to_be_planted(user_id):
    plants = retrieve_a_users_plants(user_id).exclude(plant_zone__calendar__icontains='S')
    return [plant for plant in plants if not plant.date_planted]

#get plants/slots that need to be date_harvested
def plants_to_be_harvested(user_id):
    plants = retrieve_a_users_plants(user_id)
    return [plant for plant in plants if plant.date_planted and not plant.date_harvested]

#alternative to running the above individually to get all statuses(yes it is a word)
#it will return a tuple containing 5 lists
def current_status_of_all_user_plants(user_id):
    to_be_scheduled,to_be_seeded, to_be_transplanted, to_be_planted, to_be_harvested, harvested_plants = [],[],[],[],[],[]
    plants = retrieve_a_users_plants(user_id)
    for plant in plants:
        if not plant.created_at:
            to_be_scheduled.append(plant)
        if "S" in plant.plant_zone.calendar and not plant.date_seeded:
            to_be_seeded.append(plant)
        elif "S" in plant.plant_zone.calendar and not plant.date_planted:
            to_be_transplanted.append(plant)
        elif not plant.date_planted:
            to_be_planted.append(plant)
        elif not plant.date_harvested:
            to_be_harvested.append(plant)
        else:
            harvested_plants.append(plant)
    return (to_be_scheduled, to_be_seeded, to_be_transplanted, to_be_planted, to_be_harvested, harvested_plants)

#common helper function to determine which plants can be planted or seeded this month and that the user doesn't already have in there inventory
def new_suggested_plant_activities_this_month(user_id, zone_object, p_or_s):
    all_plants_meeting_criteria = set()
    today=timezone.now()
    month=today.month - 1
    plants_in_zone = zone_object.all_plants_in_a_zone()
    for plant in plants_in_zone:
        calendar = plant.calendar.split(',')
        if calendar[month] == p_or_s:
            all_plants_meeting_criteria.add(plant)
    plants_user_already_has = set(retrieve_a_users_plants(user_id))
    results = all_plants_meeting_criteria.difference(plants_user_already_has)
    return list(results)

#which new plants in zone can be seeded this month
def plants_that_can_be_seeded_this_month(user_id, zone_object):
    return new_suggested_plant_activities_this_month(user_id, zone_object, "S")

#which plants can be seeded this month
def plants_that_can_be_planted_this_month(user_id, zone_object):
    return new_suggested_plant_activities_this_month(user_id, zone_object, "P")

#which plants could be grown at some point throughout the year in a specific zone
def all_plants_that_could_be_grown_in_this_zone(zone_object):
    return zone_object.plants.filter(calendar__icontains="P")
