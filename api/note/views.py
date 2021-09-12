from rest_framework import status, permissions, viewsets, filters as drf_filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters

from api.core.paginations import DefaultPagination
from . import serializers
from . import models


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
    queryset = models.Note.objects.none()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.NoteSerializer
    pagination_class = DefaultPagination

    filterset_class = NoteFilter
    search_fields = ("name",)
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter]

    def get_queryset(self):
        return self.request.user.notes.all()

    @action(detail=True, methods=["post"])
    def add_user(self, request):
        """
        users: [<username>,]
        """

        return Response(
            data={"message": "User added."}, status=status.HTTP_400_BAD_REQUEST
        )
