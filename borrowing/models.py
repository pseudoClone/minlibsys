from django.db import models
from uuid import uuid4
from django.utils import timezone
from django.core.exceptions import ValidationError


class Borrowing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    member = models.ForeignKey(
        "member.User", on_delete=models.CASCADE, related_name="borrowings"
    )
    book_copy = models.ForeignKey(
        "book.BookCopy", on_delete=models.CASCADE, related_name="borrowings"
    )
    borrowed_at = models.DateTimeField(default=timezone.now)
    expected_return_at = models.DateTimeField()
    returned_at = models.DateTimeField(blank=True, null=True)
    renewal_count = models.SmallIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.member.email} borrowing {self.book_copy}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["book_copy"],
                condition=models.Q(returned_at__isnull=True),
                name="one_borrow_per_copy_unless_returned",
            )
        ]

    def clean(self):
        super().clean()

        """ Expected date being greater than borrowed date implies 
        that it is in future, right? In hands of god
        """
        if self.borrowed_at and self.expected_return_at:
            if self.borrowed_at >= self.expected_return_at:
                raise ValidationError(
                    "Expected Return date and time must be greater than borrowed date and time"
                )
