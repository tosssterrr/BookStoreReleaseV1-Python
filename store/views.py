from django.db.models import Count, Case, When, Avg
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import View
from django.views.generic import ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .filters import ProductFilter
from .models import Book, Category, UserBookRelation
from .serializers import BooksSerializer, UserBookRelationSerializer, CategorySerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))
        ).select_related('author', 'category').prefetch_related('readers')
    serializer_class = BooksSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'author__name', 'category__name']
    ordering_fields = ['price', 'name', 'rating', 'annotated_likes']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        return obj


def books_main(request):
    return render(request, 'mainpage.html')


def books_detail(request):
    return render(request, 'detailpage.html')


def books_search(request):
    return render(request, 'searchpage.html')

# class HomePageView(ListView):
#     template_name = 'homepage.html'
#     context_object_name = 'books'
#     extra_context = {'title': "Главная", 'nodes': Category.objects.all()}
#     paginate_by = 3
#
#     def get_queryset(self):
#         return Book.objects.filter().select_related('author').order_by('-id')


# class DetailCategoryView(ListView):
#     template_name = 'homepage.html'
#     model = Book
#     context_object_name = 'books'
#     extra_context = {'nodes': Category.objects.all()}
#     paginate_by = 20
#
#     def get_queryset(self):
#         self.extra_context['title'] = get_object_or_404(Category, slug=self.kwargs['slug']).name
#         category = get_object_or_404(Category, slug=self.kwargs['slug']).get_descendants(include_self=True)
#         return get_list_or_404(self.model.objects.select_related('author').order_by('-id'), category__in=category)
#
#
# class DetailAuthorView(ListView):
#     template_name = 'homepage.html'
#     model = Book
#     context_object_name = 'books'
#     extra_context = {'nodes': Category.objects.all()}
#
#     def get_queryset(self):
#         self.extra_context['title'] = get_object_or_404(Author, slug=self.kwargs['slug'])
#         return get_list_or_404(self.model.objects.select_related('author'), author__slug=self.kwargs['slug'])
#
#
# class DetailBookView(View):
#     template_name = 'detailbook.html'
#     model = Book
#
#     def get(self, request, *args, **kwargs):
#         book = get_object_or_404(self.model.objects.select_related(
#             'author',
#             'category',
#         ), slug=self.kwargs['slug'])
#         context = {'book': book,
#                    'categories': book.category.get_family(),
#                    'nodes': Category.objects.all(),
#                    'cart_book_form': CartAddBookForm()}
#         return render(request, template_name=self.template_name, context=context)
#
#
# class Searching(ListView):
#     template_name = 'searchform.html'
#     context_object_name = 'books'
#     extra_context = {'nodes': Category.objects.all()}
#     paginate_by = 4
#
#     def get_queryset(self):
#         if len(self.request.GET) == 1:
#             search = Book.objects.filter(name__icontains=self.request.GET.get('q'))
#         else:
#             if self.request.GET.get('category') != 'Все':
#                 print(self.request.GET.get('category'))
#                 category = get_object_or_404(Category, slug=self.request.GET.get('category')).get_descendants(include_self=True)
#             else:
#                 category = Category.objects.all()
#             search = Book.objects.filter(
#                 name__icontains=self.request.GET.get('q'),
#                 price__gt=self.request.GET.get('min'),
#                 price__lt=self.request.GET.get('max'),
#                 year__gt=self.request.GET.get('minyear'),
#                 year__lt=int(self.request.GET.get('maxyear')) + 1,
#                 author__name__icontains=self.request.GET.get('author'),
#                 category__in=category
#             ).select_related('author').order_by('-id')
#         return search
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['q'] = self.request.GET.get('q')
#         context['min'] = self.request.GET.get('min') if 'min' in self.request.GET else 0
#         context['max'] = self.request.GET.get('max') if 'max' in self.request.GET else 10000
#         context['minyear'] = self.request.GET.get('minyear') if 'minyear' in self.request.GET else 1814
#         context['maxyear'] = self.request.GET.get('maxyear') if 'maxyear' in self.request.GET else 2022
#         context['author'] = self.request.GET.get('author') if 'author' in self.request.GET else ''
#         context['title'] = 'Поиск по вашему запросу ' + self.request.GET.get('q')
#         return context
