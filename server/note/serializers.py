from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from account.serializers import UserMinimalSerializer
from . import models


class NoteSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_profile = UserMinimalSerializer(read_only=True, source="owner")

    viewers = serializers.SerializerMethodField()

    def get_viewers(self, instance):
        return UserMinimalSerializer(instance.share_with.all(), many=True).data

    class Meta:
        model = models.Note
        fields = [
            "tags",
            "name",
            "content",
            "slug",
            "owner",
            "owner_profile",
            "viewers",
        ]
        extra_kwargs = {"slug": {"read_only": True}}


class NoteListSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    owner = UserMinimalSerializer(read_only=True)

    class Meta:
        model = models.Note
        fields = [
            "name",
            "short_content",
            "slug",
            "tags",
            "owner",
        ]
