from member.models import User  # For Pyright TypeHints, broken still
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
from .models import Borrowing


# Why service? Check reproduction docs
class BorrowingService:
    @staticmethod
    def validate_if_user_eligible(member: User):
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
        return Borrowing.objects.create(
            member=member,
            book_copy=book_copy,
            borrowed_at=borrowed_at,
            expected_return_at=expected_return_at,
        )

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
