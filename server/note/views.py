from django.contrib.auth import get_user_model
from rest_framework import status, permissions, viewsets, filters as drf_filters
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters import rest_framework as filters

from core.paginations import DefaultPagination
from . import serializers
from . import models

User = get_user_model()


class TagsFilter(filters.CharFilter):
    def filter(self, qs, value):
        if value:
            tags = [tag.strip() for tag in value.split(",")]
            qs = qs.filter(tags__name__in=tags).distinct()
        return qs


class NoteFilter(filters.FilterSet):
    tags = TagsFilter(field_name="tags__name")
    name = filters.CharFilter(lookup_expr="icontains")
    created_from = filters.CharFilter(field_name="created_at", lookup_expr="gte")
    created_to = filters.CharFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = models.Note
        fields = ["tags", "name", "created_from", "created_to"]


class NoteViewSet(viewsets.ModelViewSet):
    lookup_field = "slug"
    queryset = models.Note.objects.none()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.NoteSerializer
    pagination_class = DefaultPagination

    filterset_class = NoteFilter
    search_fields = ("name",)
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter]

    def get_queryset(self):
        return self.request.user.notes.all()

    def get_serializer_class(self):
        return (
            serializers.NoteListSerializer
            if self.action == "list"
            else serializers.NoteSerializer
        )

    @action(detail=True, methods=["post"])
    def add_user(self, request, *args, **kwargs):
        """
        users: [<username>,]
        """
        username_list = request.data.get("users")
        users = User.objects.filter(username__in=username_list)
        note = self.get_object()

        existing_users = list(note.share_with.values_list("id", flat=True)) + [
            request.user.id
        ]
        users = users.exclude(id__in=existing_users)

        for user in users:
            models.ShareWith.objects.create(
                user=user,
                note=note,
            )
        # note.share_with.add(*list(users.values_list("id", flat=True)))
        return Response(data={"message": "User added."}, status=status.HTTP_201_CREATED)


class ShareNoteReadOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = models.Note.objects.none()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.NoteSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        return self.request.user.notes.all()

    def get_serializer_class(self):
        return (
            serializers.NoteListSerializer
            if self.action == "list"
            else serializers.NoteSerializer
        )
