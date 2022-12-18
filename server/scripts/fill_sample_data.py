from apps.chat.factories import MessageFactory
from apps.events.factories import EventFactory, InviteFactory
from apps.users.factories import UserFactory

COUNT_EVENTS = COUNT_USERS = COUNT_MESSAGES = 10


def run():
    """Generate examples."""
    events = EventFactory.create_batch(size=COUNT_EVENTS)
    users = UserFactory.create_batch(size=COUNT_USERS)
    for event, user in zip(events, users):
        for _ in range(COUNT_MESSAGES):
            MessageFactory.create(event=event, user=user)
        InviteFactory.create(event=event, user=user)
        event.members.add(user)
