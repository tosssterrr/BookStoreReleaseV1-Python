from rest_framework import serializers
from rest_framework.fields import DateTimeField
from rest_framework.serializers import ModelSerializer

from store.models import Book
from .models import Order, OrderBook


class OrderBookSerializer(ModelSerializer):
    book_name = serializers.CharField(source='book.name', read_only=True)
    img = serializers.ImageField(source='book.img', read_only=True)
    price = serializers.DecimalField(source='book.price', read_only=True, max_digits=9, decimal_places=2)
    author_name = serializers.CharField(source='book.author.name', read_only=True)

    class Meta:
        model = OrderBook
        fields = ('pk', 'book', 'owner', 'qty', 'price', 'final_price', 'order', 'book_name', 'img', 'author_name')


class OrderOwnerBookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'img')


class OrderSerializer(ModelSerializer):
    created_at = DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    products = OrderOwnerBookSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('pk', 'owner', 'in_order', 'total_price', 'payment', 'created_at', 'products')
