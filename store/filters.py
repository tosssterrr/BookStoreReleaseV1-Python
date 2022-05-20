from django_filters import rest_framework as filters
from .models import Book


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    min_year = filters.NumberFilter(field_name='year', lookup_expr='gte')
    max_year = filters.NumberFilter(field_name='year', lookup_expr='lte')

    author__name = filters.CharFilter(field_name='author__name', lookup_expr='icontains')

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['min_price', 'max_price', 'min_year', 'max_year', 'name', 'author__name', 'category__name']

