from django.contrib import admin
from .models import Author, Category, Book, User, UserBookRelation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'phone', 'email')


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'slug', 'parent']


@admin.register(Book)
class BooksAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    search_fields = ['name']
    list_display = ('name', 'author', 'category')


admin.site.register(Author)
admin.site.register(UserBookRelation)
admin.site.register(Category, CategoryAdmin)

