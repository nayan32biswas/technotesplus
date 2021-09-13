from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from account.serializers import UserMinimalSerializer
from . import models


class NoteSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_profile = UserMinimalSerializer(read_only=True, source="owner")

    class Meta:
        model = models.Note
        fields = [
            "tags",
            "name",
            "content",
            "slug",
            "owner",
            "owner_profile",
        ]
        extra_kwargs = {"slug": {"read_only": True}}


class NoteListSerializer(serializers.ModelSerializer):
    owner = UserMinimalSerializer(read_only=True)

    class Meta:
        model = models.Note
        fields = [
            "name",
            "short_content",
            "slug",
            "owner",
        ]
