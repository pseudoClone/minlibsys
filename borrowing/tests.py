from django.test import TestCase
from author.models import Author
from book.models import Book, BookCopy
from member.models import User
from .services import BorrowingService
from django.core.exceptions import ValidationError


class SetupBorrowingTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="Homer")
        self.book = Book.objects.create(
            title="The Odyssey", isbn=" 9780393356250"
        )
        self.book.authors.add(self.author)

        self.copies = [
            BookCopy.objects.create(book=self.book, book_uid=f"Copy{i + 1}")
            for i in range(5)
        ]
        self.member = User.objects.create_user(
            username="apsara", email="apsara@apsara.com", password="apsara123"
        )
        self.member2 = User.objects.create_user(
            username="thakur", email="thakur@thakur.com", password="thakur123"
        )


class SetupBorrowingServiceTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name="Homer")
        self.book = Book.objects.create(
            title="The Odyssey", isbn="9780393356250"
        )
        self.book.authors.add(self.author)

        self.copies = [
            BookCopy.objects.create(book=self.book, book_uid=f"Copy{i + 1}")
            for i in range(5)
        ]
        self.member = User.objects.create_user(
            username="apsara", email="apsara@apsara.com", password="apsara123"
        )
        self.member2 = User.objects.create_user(
            username="thakur", email="thakur@thakur.com", password="thakur123"
        )

    def test_borrowing(self):
        borrowing = BorrowingService.borrow_book(
            member=self.member, book_copy=self.copies[0]
        )
        self.assertIsNotNone(borrowing.id)
        self.assertEqual(borrowing.member, self.member)
        self.assertEqual(borrowing.book_copy, self.copies[0])
        self.assertEqual(borrowing.renewal_count, 0)
        self.assertIsNone(borrowing.returned_at)

    def test_dual_borrow(self):
        BorrowingService.borrow_book(
            member=self.member, book_copy=self.copies[1]
        )
        with self.assertRaises(ValidationError):
            BorrowingService.borrow_book(
                member=self.member2, book_copy=self.copies[1]
            )
