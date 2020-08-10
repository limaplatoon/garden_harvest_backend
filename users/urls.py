from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import UserCreate, UserUpdate, HelloView, \
    LogoutAndBlacklistRefreshTokenForUserView, CustomTokenObtainPairView

urlpatterns = [
    path('user/create/', UserCreate.as_view(), name='create_user'),
    path('user/update/', UserUpdate.as_view(), name='update_user'),
    path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
    path('hello/', HelloView.as_view(), name='hello')
]
