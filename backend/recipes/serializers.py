from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.serializers import CustomUserSerializer

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('__all__')


class IngredientListSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='ingred.id')
    ingredient = serializers.CharField(source='ingred.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingred.measurement_unit', read_only=True)
    amount = serializers.IntegerField()


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

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients_amount')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        ingredients = []
        for ingredient_data in ingredients_data:
            ingredient_instance = Ingredient.objects.get(
                id=ingredient_data['ingred']['id'])
            ingredient_amount = IngredientAmount.objects.create(
                recipe_id=recipe,
                ingred=ingredient_instance,
                amount=ingredient_data['amount'])
            ingredient_amount.save()
            ingredients.append(ingredient_amount)
        recipe.ingredients_amount.set(ingredients)
        recipe.save()
        return recipe

    def update(self, recipe, validated_data):
        ingredients_data = validated_data.pop('ingredients_amount', None)
        tags_data = validated_data.pop('tags', None)
        ingredients_amount = recipe.ingredients_amount
        tags = recipe.tags.all().values('id')
        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)
        recipe.save()
        # if not tags_data:
        #     tags_list=[]
        #     for tag in tags:
        #         tags_list.append(tag['id'])
        #     recipe.tags.set(tags_list)
        if tags_data:
            recipe.tags.set(tags)
        if ingredients_amount:
            ingredients = []
            for ingredient_data in ingredients_data:
                ingredient_instance = Ingredient.objects.get(
                    id=ingredient_data['ingred']['id'])
                ingredient_amount = IngredientAmount.objects.create(
                    recipe_id=recipe,
                    ingred=ingredient_instance,
                    amount=ingredient_data['amount'])
                ingredient_amount.save()
                ingredients.append(ingredient_amount)
            recipe.ingredients_amount.set(ingredients)
        recipe.save()
        return recipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='recipe_id.name')
    image = Base64ImageField(source='recipe_id.image')
    cooking_time = serializers.ReadOnlyField(source='recipe_id.cooking_time')

    def validate_id(self, value):
        in_purchases = ShoppingCart.objects.get(recipe_id=value).exists()
        if in_purchases:
            raise ValidationError('Рецепт уже добавлен в корзину')
        return value

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')
