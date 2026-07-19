from rest_framework import viewsets
from .serializers import BooksViewSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Book


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BooksViewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.with_availability().prefetch_related("authors")
