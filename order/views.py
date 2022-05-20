from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .permissions import IsOwnerOrAdmin
from .serializers import OrderSerializer, OrderBookSerializer
from order.models import OrderBook, Order
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin, RetrieveModelMixin, ListModelMixin


class OrderBookViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    permission_classes = [IsOwnerOrAdmin]
    queryset = OrderBook.objects.all().select_related('book', 'book__author')
    serializer_class = OrderBookSerializer

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class CuurentBooksOrderViewSet(GenericViewSet, ListModelMixin):
    permission_classes = [IsOwnerOrAdmin]
    queryset = OrderBook.objects.all()
    serializer_class = OrderBookSerializer

    def list(self, request, *args, **kwargs):
        queryset = OrderBook.objects.filter(owner=request.user, order=kwargs['order']).select_related('book',
                                                                                                      'book__author')
        if queryset:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        raise PermissionDenied()


class OrderViewSet(GenericViewSet, CreateModelMixin, UpdateModelMixin,
                   DestroyModelMixin, RetrieveModelMixin, ListModelMixin):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Order.objects.all().select_related('owner')
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            queryset = Order.objects.filter(owner=request.user.pk)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(data=None)


def cart(request):
    return render(request, 'cart/cart.html')


def create_order(request):
    return render(request, 'cart/complete_order.html')



