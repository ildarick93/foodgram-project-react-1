from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer
from djoser.conf import settings
User = get_user_model()

class SubscribeField(serializers.Field):

    def to_representation(self, value):
        user_id = self.context.get('request').user.id
        if value.filter(subscriber=user_id):
            return True
        return False


class CustomUserSerializer(UserSerializer):
    is_subscribed = SubscribeField(source='subscribed_to')

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = (settings.LOGIN_FIELD, )


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'first_name',
            'last_name',
            "password",
        )