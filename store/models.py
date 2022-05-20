from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=False,
    )
    email = models.EmailField(verbose_name='E-mail', unique=True)
    phone = PhoneNumberField(verbose_name='Телефон', unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return self.username


class Book(models.Model):
    name = models.CharField(verbose_name='Название книги', max_length=255)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey('Author', on_delete=models.PROTECT, blank=True, null=True)
    category = TreeForeignKey('Category', on_delete=models.PROTECT, default=None,
                              related_name='category', blank=True, null=True)
    img = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение книги', blank=True, max_length=100)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание', max_length=10000, blank=True)

    year = models.PositiveIntegerField(verbose_name='Год издания')
    series = models.CharField(max_length=255, blank=True, null=True)
    house = models.CharField(max_length=255, blank=True, null=True)

    readers = models.ManyToManyField(User, through='UserBookRelation')

    rating = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)

    def __str__(self):
        return f'Книга - {self.name}. Автор - {self.author}. Категория - {self.category}.'

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={'slug': self.slug})


class Author(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(verbose_name='ФИО', max_length=255, blank=True)
    img = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение автора', blank=True, max_length=100)
    description = models.TextField(verbose_name='Об авторе', max_length=10000, blank=True)

    def __str__(self):
        return f'Автор - {self.name}'

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={'slug': self.slug})


class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name="children", on_delete=models.PROTECT, verbose_name='Родитель')
    slug = models.SlugField(unique=True)
    name = models.CharField(verbose_name='Имя категории', max_length=255)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={'slug': self.slug})

    class Meta:
        db_table = 'category'
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'
        ordering = ('tree_id', 'level')


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveIntegerField(choices=RATE_CHOICES, blank=True, null=True)

    def save(self, *args, **kwargs):
        from store.cache_logic import set_rating

        creating = not self.pk
        old_rating = self.rate

        super().save(*args, **kwargs)

        new_rating = self.rate
        if old_rating != new_rating or creating:
            set_rating(self.book)


