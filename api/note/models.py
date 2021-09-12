from django.db import models
from django.contrib.auth import get_user_model

from core.utils import create_slug

User = get_user_model()


class ShareWith(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="share")
    note = models.ForeignKey("Note", on_delete=models.CASCADE, related_name="share")
    view = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "note")


class Note(models.Model):
    owner = models.ForeignKey(User, related_name="notes", on_delete=models.CASCADE)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    share_with = models.ManyToManyField(
        User,
        related_name="share_notes",
        through="ShareWith",
        through_fields=("note", "user"),
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = create_slug(Note, source_data=self.name, dest_field="slug")
        return super().save(*args, **kwargs)
