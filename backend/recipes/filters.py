from django.contrib.auth import get_user_model
from django_filters import FilterSet, filters
from rest_framework.filters import SearchFilter

from .models import Recipe, Tag

User = get_user_model()


class RecipeFilterSet(FilterSet):
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug')
    is_favorited = filters.BooleanFilter(
        label="Favorited",
        method='filter_is_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        label="Is in shopping cart",
        method='filter_is_in_shopping_cart')
#
    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']

    def filter_is_favorite(self, queryset, name, value):
        return Recipe.objects.filter(favorites__user_id=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return Recipe.objects.filter(purchases__user_id=self.request.user)


class CustomSearchFilter(SearchFilter):
    search_param = "name"
