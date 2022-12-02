from datetime import datetime, timedelta

import factory
import pytz

from apps.events import models
from apps.users.factories import UserFactory


class EventFactory(factory.django.DjangoModelFactory):
    """Factory for Event model."""

    name = factory.Faker("name")
    description = factory.Faker("catch_phrase")
    address = factory.Faker("address")
    datetime_spending = factory.LazyAttribute(
        lambda _: datetime.now(pytz.UTC) + timedelta(days=2),
    )
    is_online = factory.Faker("pybool")
    is_private = factory.Faker("pybool")
    is_finished = factory.Faker("pybool")
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = models.Event


class InviteFactory(factory.django.DjangoModelFactory):
    """Factory for Invite model."""

    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventFactory)
    is_accepted = factory.Faker("pybool")
    is_active = factory.Faker("pybool")

    class Meta:
        model = models.Invite
