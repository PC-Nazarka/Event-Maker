from datetime import datetime, timedelta

import factory
import pytz

from apps.events.models import Event
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
        model = Event
