from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation, User, Category


class BooksReaderSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BooksSerializer(ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    author_name = serializers.CharField(source='author.name', default='', read_only=True)
    category_name = serializers.CharField(source='category.name', default='', read_only=True)

    readers = BooksReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'name', 'slug', 'author', 'author_name', 'category_name',
                  'category', 'annotated_likes', 'rating', 'price', 'img',
                  'description', 'year', 'series', 'house', 'readers')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug', 'name')


class UserBookRelationSerializer(ModelSerializer):

    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks', 'rate')
