from django.db import models
from uuid import uuid4
from django.core.validators import RegexValidator, MinLengthValidator


class Book(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    isbn = models.CharField(
        max_length=13,
        validators=[
            RegexValidator(
                r"^[0-9]+$",
                message="Insert only the correct ISBN with numbers",
            ),
            MinLengthValidator(10, message="ISBN is typically 10-13 digits"),
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
