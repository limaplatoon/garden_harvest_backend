from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=1, write_only=True)
    zip_code = serializers.CharField(required=True, min_length=5, max_length=5)
    zone = serializers.CharField(required=True, min_length=2, max_length=3)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'username', 'password', 'zip_code', 'zone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
