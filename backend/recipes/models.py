from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name =  models.CharField(
        max_length=200,
        verbose_name='Название тега')
    color = models.CharField(
        max_length=7,
        null=True, 
        blank=True)
    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes')
    ingridients = models.ManyToManyField(Ingredient, through='IngredientAmount')
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    name = models.CharField(
        max_length=200)
    image = models.ImageField(upload_to='eat-photo', null=True)
    text = models.CharField(
        max_length=200
    )
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.name

class IngredientAmount(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        verbose_name='Ингредиент',
        null=True,
        blank=True)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
        related_name='ingredients')
    amount = models.IntegerField(
        verbose_name='Количество'
    )