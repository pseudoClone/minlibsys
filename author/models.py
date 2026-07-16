from django.db import models
from uuid import uuid4


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=63)
    middle_name = models.CharField(max_length=63, blank=True)
    last_name = models.CharField(max_length=63, blank=True)

    def __str__(self) -> str:
        return " ".join(
            filter(None, [self.first_name, self.middle_name, self.last_name])
        )
