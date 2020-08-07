from django.urls import path, include
from .views import ListAvailablePlants

urlpatterns = [
    path('suggested/', ListAvailablePlants.as_view())
]
