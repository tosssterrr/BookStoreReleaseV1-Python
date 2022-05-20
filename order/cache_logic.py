from decimal import Decimal

from django.db.models import Sum

from .models import OrderBook


def set_total_price(order):
    total_price = OrderBook.objects.filter(order=order).aggregate(Sum('final_price')).get('final_price__sum')
    return total_price if total_price else 0



