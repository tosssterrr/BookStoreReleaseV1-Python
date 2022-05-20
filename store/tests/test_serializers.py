from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Category, Author, Book, User, UserBookRelation
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):

    def test_ok(self):
        self.user_1 = User.objects.create(username='test user 1', email='test1@email.com', phone='+79315962631',
                                          first_name='Антон', last_name='Ерохов')
        self.user_2 = User.objects.create(username='test user 2', email='test2@email.com', phone='+79315962632',
                                          first_name='Андрей', last_name='Марков')
        self.user_3 = User.objects.create(username='test user 2', email='test3@email.com', phone='+79315962633',
                                          first_name='Алексей', last_name='Панин')

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
        UserBookRelation.objects.create(user=self.user_1, book=self.book_1, like=True, rate=5)
        UserBookRelation.objects.create(user=self.user_2, book=self.book_1, like=True, rate=6)
        user_book_3 = UserBookRelation.objects.create(user=self.user_3, book=self.book_1, like=True)
        user_book_3.rate = 4
        user_book_3.save()

        UserBookRelation.objects.create(user=self.user_1, book=self.book_2, like=True, rate=3)
        UserBookRelation.objects.create(user=self.user_2, book=self.book_2, like=True, rate=7)
        UserBookRelation.objects.create(user=self.user_3, book=self.book_2, like=False)

        books = Book.objects.filter(id__in=[self.book_1.id, self.book_2.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        )
        data = BooksSerializer(books, many=True).data
        print(data)
        expected_data = [
            {
                'id': self.book_1.id,
                'name': '1984',
                'slug': '1984',
                'author': self.book_1.author.pk,
                'author_name': 'Джордж Оруэлл',
                'category_name': 'Классическая зарубежная проза',
                'category': self.book_1.category.pk,
                'annotated_likes': 3,
                'rating': '5.50',
                'price': '220.00',
                'description': '',
                'year': 2021,
                'series': 'Эксклюзивная классика',
                'house': 'АСТ',
                'readers': [
                    {
                        'first_name': 'Антон',
                        'last_name': 'Ерохов',
                    },
                    {
                        'first_name': 'Андрей',
                        'last_name': 'Марков',
                    },
                    {
                        'first_name': 'Алексей',
                        'last_name': 'Панин',
                    },
                ]
            },
            {
                'id': self.book_2.id,
                'name': 'Забытый легион: роман',
                'slug': 'zabitiy-legion',
                'author': self.book_2.author.pk,
                'author_name': 'Сапковский Анджей',
                'category_name': 'Историческая зарубежная проза',
                'category': self.book_2.category.pk,
                'annotated_likes': 2,
                'rating': '5.00',
                'price': '537.00',
                'description': '',
                'year': 2022,
                'series': 'КИНО!!',
                'house': 'Popcorn Books',
                'readers': [
                    {
                        'first_name': 'Антон',
                        'last_name': 'Ерохов',
                    },
                    {
                        'first_name': 'Андрей',
                        'last_name': 'Марков',
                    },
                    {
                        'first_name': 'Алексей',
                        'last_name': 'Панин',
                    },
                ]
            },
        ]
        print(expected_data)
        self.assertEqual(expected_data, data)
