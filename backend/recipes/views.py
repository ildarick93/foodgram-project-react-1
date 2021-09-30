import io

from api.permissions import IsAuthor, ReadOnly
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import RecipeSerializer as FavoriteRecipeSerializer

from .filters import CustomSearchFilter, RecipeFilterSet
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)
from .serializers import (IngredientListSerializer, IngredientSerializer,
                          RecipeListSerializer, ShoppingCartSerializer,
                          TagSerializer)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilterSet
    serializer_class = RecipeListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['GET', 'DELETE'])
    def shopping_cart(self, request, pk=None):
        if request.method == 'GET':
            in_purchases = ShoppingCart.objects.filter(
                recipe_id=int(pk),
                user_id=self.request.user
            )
            if in_purchases.exists():
                raise ValidationError('Рецепт уже добавлен в корзину')
            recipe = Recipe.objects.get(id=int(pk))
            purchases = ShoppingCart.objects.create(
                recipe_id=recipe,
                user_id=self.request.user
            )
            purchases.save()
            serializer = ShoppingCartSerializer(purchases)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            in_purchases = get_object_or_404(
                ShoppingCart,
                recipe_id=int(pk),
                user_id=self.request.user)
            in_purchases.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'delete'])
    def favorite(self, request, pk=None):

        user = self.request.user
        if request.method == 'GET':
            in_favorites = Favorite.objects.filter(
                user_id=user.id,
                recipe_id=pk)
            if in_favorites:
                raise ValidationError(
                    detail='Рецепт уже находится в избранном')
            recipe = get_object_or_404(Recipe, id=int(pk))
            favorite = Favorite.objects.create(
                user_id=user,
                recipe_id=recipe)
            favorite.save()
            serializer = FavoriteRecipeSerializer(recipe)
            return Response(serializer.data)
        if request.method == 'DELETE':
            in_favorites = get_object_or_404(
                Favorite,
                user_id=user.id,
                recipe_id=pk
            )
            in_favorites.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        queryset = ShoppingCart.objects.filter(
            user_id=self.request.user).values(
            'recipe_id__ingredients__name',
            'recipe_id__ingredients__measurement_unit').annotate(
                Sum('recipe_id__ingredients_amount__amount'))
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        p.setLineWidth(.3)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        p.setFont('FreeSans', 14)
        t = p.beginText(30, 750, direction=0)
        t.textLine('Список покупок')
        p.line(30, 747, 580, 747)
        t.textLine(' ')
        for qs in queryset:
            title = qs['recipe_id__ingredients__name']
            amount = qs['recipe_id__ingredients_amount__amount__sum']
            mu = qs['recipe_id__ingredients__measurement_unit']
            t.textLine(f'{title} ({mu}) - {amount}')
        p.drawText(t)
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

    def get_permissions(self):
        if self.action in ['shopping_cart', 'favorite',
                           'download_shopping_cart']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthor | ReadOnly]
        return [permission() for permission in permission_classes]


class IngredientsAmountView(generics.ListAPIView):
    queryset = IngredientAmount.objects.all()
    serializer_class = IngredientListSerializer


class IngredientsViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [CustomSearchFilter, ]
    search_fields = ['^name']
    pagination_class = None
