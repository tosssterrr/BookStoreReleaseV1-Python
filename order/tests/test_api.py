import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Category, Author, Book

User = get_user_model()


class OrderBooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test user 1', email='test@email.com', phone='+79315962633')

        self.category_1 = Category.objects.create(slug='classic-zarubej', name='Классическая зарубежная проза')
        self.category_2 = Category.objects.create(slug='historical-zarubej', name='Историческая зарубежная проза')
        self.category_3 = Category.objects.create(slug='zarubej', name='Зарубежная проза')

        self.author_1 = Author.objects.create(slug='oruell', name='Джордж Оруэлл', img='')
        self.author_2 = Author.objects.create(slug='sapkovskiy', name='Сапковский Анджей', img='')
        self.author_3 = Author.objects.create(slug='london', name='Джек Лондон', img='')

        self.book_1 = Book.objects.create(name='1984', slug='1984', img='', price=220,
                                          year=2021, author=self.author_1, category=self.category_1,
                                          series='Эксклюзивная классика', house='АСТ')
        self.book_2 = Book.objects.create(name='Забытый легион: роман', slug='zabitiy-legion',
                                          img='', price=537, year=2022,
                                          author=self.author_2, category=self.category_2,
                                          series='КИНО!!', house='Popcorn Books')
        self.book_3 = Book.objects.create(name='Джек Лондон. Рассказы', slug='jack-london-rass', img='',
                                          price=220, year=2021, author=self.author_3,
                                          category=self.category_3, house='Народная асвета')
        self.book_4 = Book.objects.create(name='Мартин Иден', slug='martin-iden', img='',
                                          price=500, year=2021, author=self.author_3,
                                          category=self.category_1, house='АСТ', series='Эксклюзивная классика')

    def test_ok(self):
        url_order = reverse('order-list')
        data = {
            "owner": self.user.pk,
            "total_price": "0.00",
            "payment": "Н",
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url_order, data=json_data,
                                    content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        url_books = reverse('orderbook-list')
        data_2 = {
                "book": self.book_1.pk,
                "owner": self.user.pk,
                "qty": 1,
                "final_price": 0,
                "order": 1
            }
        json_data_2 = json.dumps(data_2)
        response_2 = self.client.post(url_books, data=json_data_2,
                                      content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response_2.status_code)
        data_3 = {
                "book": self.book_2.pk,
                "owner": self.user.pk,
                "qty": 2,
                "final_price": 0,
                "order": 1
            }
        json_data_3 = json.dumps(data_3)
        response_3 = self.client.post(url_books, data=json_data_3,
                                      content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response_3.status_code)
        url_get_order = reverse('order-detail', args=(1,))
        response_4 = self.client.get(url_get_order)
        self.assertEqual(status.HTTP_200_OK, response_4.status_code)
        print(response_4.data)
