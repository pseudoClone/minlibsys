from member.models import User  # For Pyright TypeHints, broken still
from book.models import Book, BookCopy
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction, IntegrityError
from .models import Borrowing


# Why service? Check reproduction docs
class BorrowingService:
    @staticmethod
    def validate_if_user_eligible(member: "member.models.User"):
        if not member.is_active:
            raise ValidationError(
                "User not active. Only active users can make transactions"
            )
        has_overdue = member.borrowings.filter(
            returned_at__isnull=True, expected_return_at__lt=timezone.now()
        ).exists()
        if has_overdue:
            raise ValidationError(
                "User has overdue books. Cannot make transactions until overdue books are returned"
            )
        user_borrow_count = member.borrowings.filter(
            returned_at__isnull=True
        ).count()
        if user_borrow_count >= 4:
            raise ValidationError(
                "Borrowing limit reached. Cannot borrow further"
            )

    @staticmethod
    @transaction.atomic
    def borrow_book(member, book_copy, duration_days=7) -> Borrowing:
        BorrowingService.validate_if_user_eligible(member=member)
        is_already_borrowed = Borrowing.objects.filter(
            book_copy=book_copy, returned_at__isnull=True
        ).exists()
        if is_already_borrowed:
            raise ValidationError("Book Copy already borrowed, cannot borrow")
        borrowed_at = timezone.now()
        expected_return_at = borrowed_at + timezone.timedelta(
            days=duration_days
        )
        try:
            with transaction.atomic():
                return Borrowing.objects.create(
                    member=member,
                    book_copy=book_copy,
                    borrowed_at=borrowed_at,
                    expected_return_at=expected_return_at,
                )
        except IntegrityError:
            raise ValidationError("Book copy already borrowed. Concurrency")

    @staticmethod
    @transaction.atomic
    def return_book(borrowing) -> Borrowing:
        if borrowing.returned_at is not None:
            raise ValidationError("Book already returned")
        borrowing.returned_at = timezone.now()
        borrowing.save()
        return borrowing

    @staticmethod
    @transaction.atomic
    def renew_book(borrowing, extension_in_days=4, max_renewal=1) -> Borrowing:
        if borrowing.returned_at is not None:
            raise ValidationError("Book has already been returned")
        if borrowing.expected_return_at < timezone.now():
            raise ValidationError("Cannot renew book that are overdue")
        if borrowing.renewal_count >= max_renewal:
            raise ValidationError("Book has reached max renewal limit")

        borrowing.expected_return_at += timezone.timedelta(
            days=extension_in_days
        )
        borrowing.renewal_count += 1
        borrowing.save()
        return borrowing

    @staticmethod
    def get_available_copy(book: Book) -> BookCopy:
        available_copies = (
            BookCopy.objects
            .filter(book=book)
            .exclude(borrowings__returned_at__isnull=True)
            .first()
        )
        if not available_copies:
            raise ValidationError("No copies available of this book")
        return available_copies

    @staticmethod
    def borrow_book_by_id(member, book_id, duration_days=7) -> Borrowing:
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise ValidationError("Requested book does not exist")
        book_copy = BorrowingService.get_available_copy(book=book)
        return BorrowingService.borrow_book(
            member=member, book_copy=book_copy, duration_days=duration_days
        )
