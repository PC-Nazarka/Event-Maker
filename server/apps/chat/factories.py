from datetime import datetime

import factory
import pytz

from apps.chat.models import Message
from apps.events.factories import EventFactory
from apps.users.factories import UserFactory


class MessageFactory(factory.django.DjangoModelFactory):
    """Factory for Message model."""

    created_at = factory.LazyAttribute(
        lambda _: datetime.now(pytz.UTC),
    )
    message = factory.Faker("name")
    event = factory.SubFactory(EventFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Message
