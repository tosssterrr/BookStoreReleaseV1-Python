# from decimal import Decimal
# from django.conf import settings
# from store.models import Book
#
#
# class Cart(object):
#     '''
#     Класс корзины для работы с ней в куки файлах
#     '''
#     def __init__(self, request):
#         '''
#         Создание корзины
#         :param request:
#         '''
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#         if not cart:
#             cart = self.session[settings.CART_SESSION_ID] = {}
#         self.cart = cart
#
#     def __iter__(self):
#         product_ids = self.cart.keys()
#
#         products = Book.objects.filter(id__in=product_ids)
#
#         cart = self.cart.copy()
#
#         for product in products:
#             cart[str(product.id)]['product'] = product
#
#         for item in cart.values():
#             item['price'] = Decimal(item['price'])
#             item['total_price'] = item['price'] * item['quantity']
#             yield item
#
#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def add(self, product, quantity=1, update_quantity=False):
#         '''
#         Добавление товара в корзину
#         :param product: id book
#         :param quantity: quantity books
#         :param update_quantity: обновление количества товаров
#         :return:
#         '''
#         product_id = str(product.id)
#         if product_id not in self.cart:
#             self.cart[product_id] = {'quantity': 0,
#                                      'price': str(product.price)}
#         if update_quantity:
#             self.cart[product_id]['quantity'] = quantity
#         else:
#             self.cart[product_id]['quantity'] += quantity
#         self.save()
#
#     def save(self):
#         # Сохранение корзины
#         self.session.modified = True
#
#     def remove(self, product):
#         # Удаление обьекта из корзины
#         product_id = str(product.id)
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()
#
#     def get_total_price(self):
#         return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
#
#     def clear(self):
#         # Полная очистка корзины
#         del self.session[settings.CART_SESSION_ID]
#         self.save()
#
#     def __str__(self):
#         print(self.cart)
#         return 'order'
#
#
