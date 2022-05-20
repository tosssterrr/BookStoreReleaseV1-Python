from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import cart, create_order

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('create_order/', create_order, name='order'),
]

