from rest_framework import mixins, status, generics, viewsets, filters as drf_filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.core.paginations import DefaultPagination
from . import serializers
from . import models


class RegistrationAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


class UserViewSet(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.none()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserDetailSerializer

    def get_object(self):
        return self.request.user


class PasswordViewSet(viewsets.GenericViewSet):
    queryset = models.User.objects.none()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def password_reset(self, *args, **kwargs):
        serializer = serializers.PasswordChangeSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = self.request.user
            if user.check_password(data["current_password"]):
                user.set_password(data["new_password"])
                user.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class UserListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserDetailSerializer
    pagination_class = DefaultPagination
    search_fields = ("username", "email", "first_name", "last_name")
    filter_backends = [drf_filters.SearchFilter]

    def get_object(self):
        return self.request.user
