from rest_framework import status, generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from . import serializers
from . import models


class RegistrationAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
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
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.UserDetailSerializer

    def get_object(self):
        return self.request.user


class PasswordViewSet(viewsets.GenericViewSet):
    queryset = models.User.objects.none()
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
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
