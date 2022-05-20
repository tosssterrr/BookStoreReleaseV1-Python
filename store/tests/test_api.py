import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models import Count, Case, When, Avg
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from django.contrib.contenttypes.models import ContentType
from store.models import Book, Author, Category, UserBookRelation
from store.serializers import BooksSerializer

User = get_user_model()


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test user 1', email='test@email.com', phone='+79315962633')

        permissions = [
            Permission.objects.get(name='Can view book'),
            Permission.objects.get(name='Can delete book'),
            Permission.objects.get(name='Can add book'),
            Permission.objects.get(name='Can change book'),
        ]
        self.user.user_permissions.add(*permissions)

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

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).select_related('author', 'category')
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    # старый тест - нужно переписать, тк обновил фильтрацию
    # def test_get_filter(self):
    #     url = reverse('book-list')
    #     response = self.client.get(url, data={'price': 220})
    #     books = Book.objects.filter(price=220).annotate(
    #         annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).select_related('author', 'category')
    #     serializer_data = BooksSerializer(books, many=True).data
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'Джек Лондон'})
        books = Book.objects.filter(id__in=[self.book_3.pk, self.book_4.pk]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).select_related('author', 'category')
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(4, Book.objects.all().count())
        url = reverse('book-list')
        data = {
            "name": "Programming in Python 3",
            "slug": "python_3",
            "price": 150,
            "year": 2021
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        url = reverse('book-detail', args=(5,))
        books = Book.objects.filter(id=5).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).select_related('author', 'category')
        serializer_data = BooksSerializer(books[0]).data
        response = self.client.get(url)
        self.assertEqual(5, Book.objects.all().count())
        self.assertEqual(serializer_data, response.data)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "slug": self.book_1.slug,
            "price": 200,
            "year": self.book_1.year,
            "author": self.book_1.author.pk,
            "category": self.book_1.category.pk,
            "series": self.book_1.series,
            "house": self.book_1.house
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(200, self.book_1.price)
        books = Book.objects.filter(id=self.book_1.id).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).select_related('author', 'category')
        serializer_data = BooksSerializer(books[0]).data
        response = self.client.get(url)
        self.assertEqual(serializer_data, response.data)

    def test_delete(self):
        url = reverse('book-list')
        response = self.client.get(url)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).select_related('author', 'category')
        serializer_data = BooksSerializer(books, many=True).data
        self.assertEqual(serializer_data, response.data)
        url = reverse('book-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        response = self.client.delete(url)
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer(books[1:], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_update_not_permission(self):
        self.user_2 = User.objects.create(username='test user 2', email='test2@email.com', phone='+79315962632')
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "slug": self.book_1.slug,
            "price": 200,
            "year": self.book_1.year,
            "author": self.book_1.author.pk,
            "category": self.book_1.category.pk,
            "series": self.book_1.series,
            "house": self.book_1.house
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual({'detail': ErrorDetail(string='У вас недостаточно прав для выполнения данного действия.',
                                                code='permission_denied')}, response.data)
        self.book_1.refresh_from_db()
        self.assertEqual(220, self.book_1.price)
        books = Book.objects.filter(id=self.book_1.id).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).select_related('author', 'category')
        serializer_data = BooksSerializer(books[0]).data
        response = self.client.get(url)
        self.assertEqual(serializer_data, response.data)

    def test_update_superuser(self):
        self.super_user = User.objects.create(username='superuser', email='superuser@email.com',
                                              phone='+79315962631', is_superuser=True)
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "slug": self.book_1.slug,
            "price": 200,
            "year": self.book_1.year,
            "author": self.book_1.author.pk,
            "category": self.book_1.category.pk,
            "series": self.book_1.series,
            "house": self.book_1.house
        }
        json_data = json.dumps(data)
        self.client.force_login(self.super_user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(200, self.book_1.price)
        books = Book.objects.filter(id=self.book_1.id).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))).select_related('author', 'category')
        serializer_data = BooksSerializer(books[0]).data
        response = self.client.get(url)
        self.assertEqual(serializer_data, response.data)


class BooksRelationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test user 1', email='test@email.com', phone='+79315962633')

        permissions = [
            Permission.objects.get(name='Can view book'),
            Permission.objects.get(name='Can delete book'),
            Permission.objects.get(name='Can add book'),
            Permission.objects.get(name='Can change book'),
        ]
        self.user.user_permissions.add(*permissions)

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

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        data = {
            "like": True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.like)

        data = {
            "in_bookmarks": True,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        data = {
            "rate": 3,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user, book=self.book_1)
        self.assertEqual(3, relation.rate)

    def test_rate_wrong(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        self.client.force_login(self.user)
        data = {
            "rate": 11,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, response.data)
