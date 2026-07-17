from rest_framework import serializers
from .models import Borrowing
from book.models import Book, BookCopy


class BorrowingInfoSerializer(serializers.ModelSerializer):
    member_email = serializers.EmailField(source="member.email", read_only=True)
    book_title = serializers.CharField(
        source="book_copy.book.title", read_only=True
    )
    book_uid = serializers.CharField(
        source="book_copy.book_uid", read_only=True
    )

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "member_email",
            "book_title",
            "book_uid",
            "borrowed_at",
            "expected_return_at",
            "returned_at",
            "renewal_count",
        ]


class BorrowRequestSerializer(serializers.Serializer):
    book_copy_id = serializers.UUIDField()
