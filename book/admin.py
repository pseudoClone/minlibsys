from django.contrib import admin
from .models import Book, BookCopy


class BookCopyInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "authors")
    search_fields = ("title", "authors")
    inlines = [BookCopyInline]


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ("book", "book_uid")
    search_fields = ("book_uid", "book__title")
