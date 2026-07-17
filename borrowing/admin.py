from django.contrib import admin
from .models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "book_copy",
        "borrowed_at",
        "expected_return_at",
        "renewal_count",
        "returned_at",
    )
    list_filter = ("returned_at", "borrowed_at")
    search_fields = (
        "member__username",
        "book_copy__book__title",
        "book_copy__book_uid",
    )
