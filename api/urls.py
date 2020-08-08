from django.urls import path, include
from .views import ListAvailablePlants, PlantDetail, UserPlants

urlpatterns = [
    path('suggested/', ListAvailablePlants.as_view()),
    path('plants/<int:pk>/', PlantDetail.as_view()),
    path('addplant/', UserPlants.as_view()),
    # path('mygarden/', UserGarden.as_view()),
]
