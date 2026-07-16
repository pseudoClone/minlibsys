from django.db import models
from uuid import uuid4


class Borrowing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    member = models.ForeignKey(
        "member.User", on_delete=models.CASCADE, related_name="borrowings"
    )
    book_copy = models.ForeignKey(
        "book.BookCopy", on_delete=models.CASCADE, related_name="borrowings"
    )
    borrowed_at = models.DateTimeField(auto_now_add=True)
    expected_return_at = models.DateTimeField()
    returned_at = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.member.email} borrowing {self.book_copy}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book_copy"],
                condition=models.Q(returned_at=None),
                name="one_borrow_per_copy_unless_returned",
            )
        ]
