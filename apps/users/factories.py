from django.contrib.auth import get_user_model
from factory import Faker, django

PASSWORD = "root123"


class UserFactory(django.DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    password = PASSWORD

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]
