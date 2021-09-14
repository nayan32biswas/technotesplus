from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from . import models


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(
        min_length=8,
        max_length=127,
        write_only=True,
        style={"input_type": "password"},
    )

    def validate(self, attrs):
        if models.User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError(_("User already exists."))
        if models.User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(_("User already exists."))
        return super().validate(attrs)

    def save(self, **kwargs):
        data = self.validated_data
        user = models.User.objects.create_user(
            email=data["email"], username=data["username"], password=data["password"]
        )
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

    def update(self, instance, validated_data):
        email = validated_data.get("email", None)
        username = validated_data.get("username", None)
        if email is not None and email != instance.email:
            if models.User.objects.filter(email=email).exists():
                raise serializers.ValidationError(_("User already exists."))
        if username is not None and username != instance.username:
            if models.User.objects.filter(username=username).exists():
                raise serializers.ValidationError(_("User already exists."))
        return super().update(instance, validated_data)


class UserMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "full_name",
            "username",
        )


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        min_length=8,
        max_length=127,
        write_only=True,
        style={"input_type": "password"},
    )
    new_password = serializers.CharField(
        min_length=8,
        max_length=127,
        write_only=True,
        style={"input_type": "password"},
    )
