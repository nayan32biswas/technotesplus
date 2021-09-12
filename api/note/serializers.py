from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField
from . import models


class NoteSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Note
        fields = [
            "owner",
            "content",
            "slug",
        ]
        extra_kwargs = {"slug": {"read_only": True}}
