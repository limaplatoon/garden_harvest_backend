from django.urls import path, include
from .views import ListAvailablePlants, PlantDetail, Calendar, UserPlants

urlpatterns = [
    path('suggested/', ListAvailablePlants.as_view()),
    path('plants/<int:pk>/', PlantDetail.as_view()),
    path('myplants/', UserPlants.as_view()),
    path('calendarEvents/', Calendar.as_view())
]
