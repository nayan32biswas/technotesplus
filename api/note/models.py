from functools import cached_property
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.utils.text import Truncator

from taggit.managers import TaggableManager

from core.utils import create_slug

User = get_user_model()


class Note(models.Model):
    name = models.CharField(max_length=255)
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    def __str__(self) -> str:
        return self.name

    @cached_property
    def short_content(self):
        return Truncator(self.content).words(200, html=True, truncate=" ...")

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = create_slug(Note, source_data=self.name, dest_field="slug")
        return super().save(*args, **kwargs)


class ShareWith(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="share")
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="share")
    view = models.PositiveIntegerField(default=0)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "note")


@receiver(post_save, sender=ShareWith)
def share_with_post_save_receiver(sender, instance, **kwargs):
    print("send email to user")
    pass
