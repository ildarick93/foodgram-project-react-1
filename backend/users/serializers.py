from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers

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
        fields = (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'username',
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


class RecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    image = serializers.CharField()
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionsSerializer(CustomUserSerializer):
    recipes = RecipeSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField()

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        if ret.get('recipes'):
            ret['count'] = len(ret.get('recipes'))
        else:
            ret['count'] = 0
        return ret

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            "recipes",
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj.subscribers.filter(subscriber=request.user).exists()
