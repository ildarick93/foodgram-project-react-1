from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import Follow
from .serializers import SubscriptionsSerializer

User = get_user_model()


class DjUserViewSet(UserViewSet):

    @action(detail=False, methods=('GET',))
    def subscriptions(self, request):
        user = self.request.user
        subscribed_to = user.subscribed_to.all().values_list(
            'subscribed_to_id', flat=True)
        queryset = User.objects.filter(id__in=subscribed_to)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscriptionsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=('GET', 'DELETE'))
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'GET':
            if user.id == id:
                raise ValidationError('Нельзя подписаться на себя')
            if int(id) in user.subscribed_to.all().values_list(
                    'subscribed_to', flat=True):
                raise ValidationError('Вы уже подписаны на этого автора')
            else:
                follow = Follow.objects.create(
                    subscriber=user,
                    subscribed_to=author
                )
                follow.save()
                serializer = SubscriptionsSerializer(author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            follow = get_object_or_404(
                Follow,
                subscriber=user,
                subscribed_to=author)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
