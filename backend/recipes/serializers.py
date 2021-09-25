from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Tag
User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')