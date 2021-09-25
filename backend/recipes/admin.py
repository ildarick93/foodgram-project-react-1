from django.contrib import admin
from .models import Recipe, Tag, Ingredient, IngredientAmount
# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = (
        ('name', admin.EmptyFieldListFilter),
    )

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = (
        ('author', admin.RelatedOnlyFieldListFilter),
        ('tags', admin.RelatedOnlyFieldListFilter),
        ('name', admin.EmptyFieldListFilter),
    )

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredients', 'recipe', 'amount')

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)