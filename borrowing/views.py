from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Borrowing
from .serializers import BorrowingInfoSerializer, BorrowRequestSerializer
from .services import BorrowingService
from book.models import BookCopy


class BorrowingViewSet(viewsets.ModelViewSet):
    serializer_class = BorrowingInfoSerializer

    def get_queryset(self):
        return Borrowing.objects.all().select_related(
            "member", "book_copy__book"
        )

    @action(detail=False, methods=["POST"], url_path="borrow")
    def borrow_book(self, request):
        serializer = BorrowRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            book_copy = BookCopy.objects.get(
                pk=serializer.validated_data["book_copy_id"]
            )
        except BookCopy.DoesNotExist:
            return Response(
                {"error": "Book Copy not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        borrowing = BorrowingService.borrow_book(
            member=request.user, book_copy=book_copy
        )

        response_serializer = self.get_serializer(borrowing)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="return")
    def return_book(self, request, pk=None):
        borrowing = self.get_object()
        update_borrowing = BorrowingService.return_book(borrowing)
        response_serializer = self.get_serializer(update_borrowing)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="renew")
    def renew_book(self, request, pk=None):
        borrowing = self.get_object()
        updated_borrowing = BorrowingService.renew_book(borrowing)
        response_serializer = self.get_serializer(updated_borrowing)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
