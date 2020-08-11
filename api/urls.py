from django.urls import path, include

from .views import DeletePlant, ListAvailablePlants, PlantDetail, Calendar, UserPlants, AddPlant, UpdatePlant, DetermineSchedule, book_this_plant, plant_something_new_this_month, PlantSlotStatus, WhatCanBeGrownInMyArea, Encyclopedia, SlotOptions


urlpatterns = [
    path('suggested/', ListAvailablePlants.as_view()),
    path('plants/<int:pk>/', PlantDetail.as_view()),
    path('myplants/', UserPlants.as_view()),
    path('calendarEvents/', Calendar.as_view()),
    path('addplant/<int:plant_zone_id>/', AddPlant),
    path('planting-options/<int:plant_zone_id>/', SlotOptions.as_view()),
    path('scheduleplant/<int:pk>/', DetermineSchedule.as_view()),
    path('scheduleaccepted/<int:plant_slot_id>/', book_this_plant),
    path('updateplant/<int:plant_slot_id>/', UpdatePlant),
    path('deleteplant/<int:plant_slot_id>/', DeletePlant),
    path('newActivities/', plant_something_new_this_month),
    path('allPlantStatus/', PlantSlotStatus.as_view()),
    path('whatCanBeGrown/', WhatCanBeGrownInMyArea.as_view()),
    path('encyclopedia/', Encyclopedia.as_view())
    ]

    # path('addplant/', UserPlants.as_view()),

# A user sees the dashboard (left side) options - my plants / suggested
# My Plants - a list of plants the user has already added to their garden.
# 


#add Plant to my garden => PlantSlot create view (POST request) 
#schedule this plant => (GET request - "getavailabledates/") /url/<int:pk>/ or as a post(request) then we pull infor from body
#book this plant => PlantSlot ReadUpdateDeleteView (PUT)
#update this plant => PlantSlot ReadUpdateDeleteView(PUT)
#delete this plant => PlantSlot ReadUpdateDeleteView(DEL)



    # add to my garden creates a plantSlot object based on plantzone obj, user id and assigns to user's 1st slot it will kept in memory this way under a task of needs to be planned (will have to update calendar to reflect this task status)
    #returns confirmation that it is created (201)
    #front end will need to then (force) update the my plants list or otherwise update the dashboard

    #double check that the myplants url returns a list of all plantslot objects belonging to the user be sure to pass plantSlot_ID

    #user either through a "schedule this plant button" on a card or from task list then front-end makes next api call to schedule this plant using PlantSlot_id through body of request

    # "schedule this plant" possible url = "api/scheduler"
        #retrieve plantSlot_Id abbreviated as PS from request
        #call seedplaner with (PS.plant_zone, PS.slot.user.id)
        #recieve sorted list by earliest planting time [(date, slot_object)] from above call to seedplaner
        #return options as follows (current plant_slot_id, sorted_list)

    #front_end user selects and option, makes api call to /bookthisplant body include accepted_date, accepted_slot, current plant_slot_id

    #backend /bookthisplant
        #update method
        #change current_plant_slot_id' slot to accepted_slot and update the created_at date to accepted_date
        #return confirmation or errors

    #front_end user wants to update the status of a plant from to_be_seeded to to_be_transplanted or any other update to the current plant
        #front-end api call to /updateplantstatus including plant_slot_id

    #backend /updateplantstatus
        #similar to bookthisplant it will run update method on the plant_slot_id.
            #if in to_be_seeded update the date_seeded to now
            #if in to_be_transplanted or to_be_planted....update the date_planted to now and harvest_date_max, harvest_date_min
            #if in to_be_harvested   update the date_harvested to now
        #send confirmation of update or errors


    #front_end user wants to remove a plant from their garden
        #front-end api call to /deleteplantstatus including plant_slot_id
        

    #backend /deleteplantstatus
        #delete method 
        #send confirmation of delete
    #2
    #3
    #4