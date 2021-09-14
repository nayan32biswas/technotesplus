import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model

from note.models import Note
from core.utils import rand_str

fake = Faker()
User = get_user_model()


def create_users():
    for _ in range(10):
        user = fake.simple_profile()
        try:
            User.objects.create_user(
                email=user["mail"],
                username=user["username"],
                password=rand_str(12),
                first_name=user["name"].split(" ")[0],
                last_name=user["name"].split(" ")[-1],
            )
        except Exception:
            pass


def create_notes():
    for _ in range(100):
        yield Note.objects.create(
            name=fake.name(),
            content=fake.sentence(
                nb_words=random.randint(10, 100), variable_nb_words=False
            ),
            owner=User.objects.order_by("?").first(),
        )


def share_notes():
    for note in Note.objects.order_by("?")[:20]:
        users = set(
            User.objects.order_by("?").values_list("id", flat=True)[
                : random.randint(2, 5)
            ]
        )
        if note.owner.id in users:
            users.remove(note.owner.id)
        note.share_with.add(*users)


def populate_database():
    create_users(), print("User Created")
    list(create_notes())
    share_notes()


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Database initialize")
        populate_database()
