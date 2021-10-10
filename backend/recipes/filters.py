from django.contrib.auth import get_user_model
from django_filters import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag

User = get_user_model()


class RecipeFilterSet(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='Tags')
    is_favorited = filters.BooleanFilter(
        label="Favirited",
        method='filter_is_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        label="Is in shopping cart",
        method='filter_is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ['author', 'tags']

    def filter_is_favorite(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(favorites__user_id=self.request.user)
        return Recipe.objects.all()

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(purchases__user_id=self.request.user)
        return Recipe.objects.all()


class CustomSearchFilter(SearchFilter):
    search_param = "name"
