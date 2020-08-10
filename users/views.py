from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Zone
from users.models import ZipZone
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def get_zone_from_zip(zip_code: str) -> dict:
    try:
        zip_zone = ZipZone.objects.get(zip_code=zip_code)
        zone = Zone.objects.get(zone=zip_zone.zone)
        extended_data = dict(zone=zone.pk)
    except Zone.DoesNotExist:
        extended_data = {}
    return extended_data


class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        extended_data = get_zone_from_zip(request.data['zip_code'])
        request.data.update(extended_data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdate(APIView):  # Try to consolidate to UserCreate..?
    authentication_classes = ()


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class HelloView(APIView):
    def get(self, request):
        return Response(data=dict(first_name=self.request.user.first_name,
                                  last_name=self.request.user.last_name,
                                  username=self.request.user.username,
                                  email=self.request.user.email,
                                  zip_code=self.request.user.zip_code,
                                  zone=self.request.user.zone.zone
                                  ),
                        status=status.HTTP_200_OK)
