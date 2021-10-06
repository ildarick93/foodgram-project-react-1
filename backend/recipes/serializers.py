from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from django.db.models import F
from rest_framework import serializers
from users.serializers import CustomUserSerializer
from rest_framework.serializers import ValidationError

from .models import (Favorite, IngredientAmount, Recipe, Ingredient,
                     ShoppingCart, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientListSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='ingred.id')
    name = serializers.CharField(source='ingred.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingred.measurement_unit', read_only=True)
    amount = serializers.IntegerField()


class IngredientsAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingred.id')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')


class RecipeListSerializer(serializers.ModelSerializer):
    ingredients = IngredientListSerializer(
        source='ingredients_amount', many=True)
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            recipe_id=obj, user_id=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe_id=obj,
                                           user_id=request.user).exists()

    class Meta:
        model = Recipe
        fields = ('__all__')


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientsAmountSerializer(
        source='ingredients_amount', many=True)
    name = serializers.CharField(required=False)
    text = serializers.CharField(required=False)

    class Meta:
        model = Recipe
        fields = ('__all__')

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if ingredients == []:
            raise ValidationError('Нужно выбрать как минимум 1 ингридиент!')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise ValidationError('Количество должно быть положительным!')
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise ValidationError('Время приготовления не может быть'
                                  ' отрицательным числом или нулем!')
        return data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients_amount')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        ingredients_amount = self.get_ingredients_list(
            ingredients_data, recipe)
        recipe.tags.set(tags)
        recipe.ingredients_amount.set(ingredients_amount)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients_amount', None)
        tags_data = validated_data.pop('tags', None)
        recipe = super().update(instance, validated_data)
        if tags_data:
            recipe.tags.set(tags_data)
        if ingredients_data:
            ingredients = self.get_ingredients_list(
                ingredients_data,
                recipe)
            recipe.ingredients_amount.set(ingredients)
        recipe.save()
        return recipe

    def get_ingredients_list(self, ingredients, recipe):
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['ingred']['id']
            amount = ingredient['amount']
            ingred_instance = Ingredient.objects.get(id=ingredient_id)
            if IngredientAmount.objects.\
               filter(recipe_id=recipe, ingred_id=ingredient_id).exists():
                amount += F('amount')
            ingred = IngredientAmount.objects.update_or_create(
                recipe_id=recipe, ingred=ingred_instance,
                defaults={'amount': amount})
            ingredients_list.append(ingred)
        return ingredients_list


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class ShoppingCartSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='recipe_id.name')
    image = Base64ImageField(source='recipe_id.image')
    cooking_time = serializers.ReadOnlyField(source='recipe_id.cooking_time')
