from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(lookup_expr='slug')
    category = CharFilter(lookup_expr='slug')
    name = CharFilter(lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name',)
