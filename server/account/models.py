# from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self,
        email="",
        username="",
        password=None,
        is_staff=False,
        is_active=True,
        **extra_fields,
    ):
        if not password:
            raise ValueError("User should have password.")

        user = self.model(
            email=email,
            username=username,
            is_active=is_active,
            is_staff=is_staff,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            is_active=True,
            is_staff=True,
            is_superuser=True,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    objects = UserManager()

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username
