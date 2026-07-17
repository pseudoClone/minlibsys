from django.db import models
from uuid import uuid4
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError


def validate_ISBN(ISBN: str):
    if len(ISBN) == 13:
        if not ISBN.isdigit():
            raise ValidationError("ISBN-13 must only have number")
        dsum = 0
        digits = [int(char) for char in ISBN]
        for idx, digit in enumerate(digits):
            if (idx) % 2 == 0:
                dsum += digit
            else:
                dsum += digit * 3
        if dsum % 10 != 0:
            raise ValidationError("Not a valid 13 digit ISBN")

    elif (len(ISBN)) == 10:
        dsum = 0
        for idx, char in enumerate(ISBN):
            if idx == 9 and char == "X":
                digit = 10
            elif char.isdigit():
                digit = int(char)
            else:
                raise ValidationError("Invalid characters in ISBN string")
            dsum += digit * (10 - idx)
        if dsum % 11 != 0:
            raise ValidationError("Not a valid 10 digit ISBN")
    else:
        raise ValidationError("ISBN is incorrect")


class Book(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    isbn = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                r"^(?:\d{9}[\dX]|\d{13})$",
                message="Insert only the correct ISBN with numbers",
            ),
            MinLengthValidator(10, message="ISBN is typically 10-13 digits"),
            validate_ISBN,
        ],
        unique=True,
    )
    authors = models.ManyToManyField("author.Author", related_name="books")

    def __str__(self) -> str:
        return f"{self.title}"


class BookCopy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    book = models.ForeignKey(
        Book, related_name="bookcopies", on_delete=models.CASCADE
    )
    book_uid = models.CharField(max_length=63, unique=True)
    # Globally unique in the sense that one transaction uses One Time Pad

    def __str__(self):
        return f"{self.book.title} | Copy number: {self.book_uid}"
