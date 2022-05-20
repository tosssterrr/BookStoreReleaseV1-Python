from django.contrib.auth import get_user_model
from django.db import models
from store.models import Book

User = get_user_model()
PAYMENT_TYPE_CHOICES = (('Н', 'Наличными'), ('К', 'По карте'))


class OrderBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    qty = models.PositiveIntegerField()
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая цена')
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return f'Книга "{self.book.name}" для {self.order.owner}'

    def save(self, *args, **kwargs):
        self.final_price = float(self.book.price) * self.qty
        super().save(*args, **kwargs)
        order = Order.objects.get(pk=self.order.id)
        order.save()


class Order(models.Model):
    owner = models.ForeignKey(User, null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    in_order = models.BooleanField(verbose_name='Доставлен', default=False)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Итоговая цена',
                                      blank=True, null=True)
    payment = models.CharField(choices=PAYMENT_TYPE_CHOICES, default='Н', max_length=10)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    products = models.ManyToManyField(Book, through='OrderBook')

    def __str__(self):
        return f'Заказ на имя {self.owner.first_name}, от {self.created_at.strftime("%Y-%m-%d %H:%M")}'

    def save(self, *args, **kwargs):
        from order.cache_logic import set_total_price

        creating = self.pk
        self.total_price = set_total_price(self)
        super(Order, self).save(*args, **kwargs)


