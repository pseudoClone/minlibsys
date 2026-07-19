from rest_framework import serializers
from .models import Book


class BooksViewSerializer(serializers.ModelSerializer):
    total_copies = serializers.IntegerField(read_only=True)
    available_copies = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "isbn", "total_copies", "available_copies"]
