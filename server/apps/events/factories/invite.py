import factory

from apps.events.models import Invite
from apps.users.factories import UserFactory

from .event import EventFactory


class InviteFactory(factory.django.DjangoModelFactory):
    """Factory for Invite model."""

    user = factory.SubFactory(UserFactory)
    event = factory.SubFactory(EventFactory)
    is_accepted = factory.Faker("pybool")
    is_active = factory.Faker("pybool")

    class Meta:
        model = Invite
