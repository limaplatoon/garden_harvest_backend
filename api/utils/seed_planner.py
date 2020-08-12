'''
This is the seeding algorithm to determine the earliest available start date in
each user slot. Given that there are 0 or more plants already scheduled within 
each slot; this determines when a plant can be scheduled to start seeding(if 
the plant requires seeding) or planting.

It first pulls down a list of all of the user's slots. For each slot, it filters 
out plants that have already be harvested and sorts them chronologically by 
start or planned start date. Additionally, it must adhere to the constraint that
most plants can not be seeded or planted year-round and have a growing season.

If a slot is empty, it will find the first available date within the plant's 
growing season. If a slot has existing plants, it will check to see if the plant 
has time for it's life-cycle to be completed between existing plant schedules 
and then check to see if a found gap is within the plant's growing season. If it 
can not be scheduled between existing plant schedules, it will find the first 
available date within the plant's growing season after the last scheduled plant's 
expected life-cycle completes.

finally, it will return the list of user slots in ascending order based on the 
earliest proposed start date.
'''

from django.utils import timezone
from datetime import datetime
from api.models import PlantSlot, Slot


def depends_on_season(proposed_date, month, plant_obj, p_or_s):
    year= proposed_date.year
    calendar = plant_obj.calendar.split(',')
    adj_calendar = calendar[month:] + calendar[:month]
    adj_month = adj_calendar.index(p_or_s) + 1
    planned_date = timezone.make_aware(timezone.datetime((year + (month + adj_month)//12),((month + adj_month)%12),1,0,0,0,0))
    return planned_date

def retrieve_event_information(event):
    plant = event.plant_zone.plant
    calendar = event.plant_zone.calendar
    if event.date_planted:
        start_date = timezone.make_aware(datetime.combine(event.created_at, datetime.min.time()))
        end_date = timezone.make_aware(datetime.combine(event.harvest_date_max, datetime.min.time()))
    else:
        start_date = timezone.make_aware(datetime.combine(event.created_at, datetime.min.time()))
        time_delta = (timezone.timedelta(days=(plant.harvest_max + (56 if "S" in calendar else 14))))
        end_date = start_date + time_delta
    return start_date, end_date

def placement(plant_obj, existing_plant_schedule):
    p_or_s = "S" if "S" in plant_obj.calendar else "P"
    proposed_date = timezone.now()
    month = (proposed_date.month - 1)
    time_delta = timezone.timedelta(days=(plant_obj.plant.harvest_max + (56 if "S" in p_or_s else 14)))
    index = 0
    slot_not_found = True
    while slot_not_found and (index < len(existing_plant_schedule)):
        event = existing_plant_schedule[index]
        scheduled_start, scheduled_end = retrieve_event_information(event)
        if proposed_date + time_delta <= scheduled_start:
            if p_or_s in plant_obj.calendar.split(',')[month]:
                slot_not_found = False
        if slot_not_found:
            proposed_date = scheduled_end
        index += 1
    if slot_not_found:
        earliest_available = depends_on_season(proposed_date, month, plant_obj, p_or_s)
    else:
        earliest_available = proposed_date
    return earliest_available

def schedule(plant_obj, user_id):
    slots = list(Slot.objects.filter(user__id=user_id))
    earliest_slot_times = []
    for slot in slots:
        existing_plant_schedule = list(PlantSlot.objects.filter(slot__id=slot.id).exclude(date_harvested__isnull=False).order_by('created_at'))
        result = placement(plant_obj, existing_plant_schedule)
        slot_details = {'pk': slot.id, 'color': slot.color, 'location_description': slot.location_description, 'name': slot.name, 'user': slot.user.id}
        earliest_slot_times.append((result, {'slot': slot_details}))
    proposals = sorted(earliest_slot_times, key=lambda x: x[0])
    return proposals


def schedule_by_slot(slot, plant_zone):
    existing_plant_schedule = PlantSlot.objects.filter(
        slot__id=slot.id
    ).exclude(date_harvested__isnull=False).order_by('created_at')
    result = placement(plant_zone, existing_plant_schedule)
    return result
