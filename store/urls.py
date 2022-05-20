from django.urls import path
from rest_framework.routers import SimpleRouter

from order.views import OrderViewSet, OrderBookViewSet, CuurentBooksOrderViewSet
from .views import BookViewSet, UserBookRelationView, CategoryViewSet, books_main, books_detail, books_search
from django.conf.urls.static import static
from django.conf import settings

router = SimpleRouter()

router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBookRelationView)
router.register(r'category', CategoryViewSet)
router.register(r'order_book', OrderBookViewSet)
router.register(r'order', OrderViewSet)


urlpatterns = [
    path('', books_main, name='home'),
    path('book_current/', books_detail),
    path('book_search/', books_search),
    path(r'books_order/<int:order>', CuurentBooksOrderViewSet.as_view({'get': 'list'}))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
