from channels.db import database_sync_to_async
from django.db.models import QuerySet

from apps.chat.models import Message
from apps.events.models import Event


class EventQueries:

    @staticmethod
    @database_sync_to_async
    def get_members_list(event_id: int) -> QuerySet:
        return Event.objects.prefetch_related(
            "members",
        ).get(id=event_id).members.all()

    @staticmethod
    @database_sync_to_async
    def check_event_exists(event_id: int) -> bool:
        return Event.objects.filter(id=event_id).exists()

    @staticmethod
    @database_sync_to_async
    def check_user_consist_in_event(user_id: int, event_id: int) -> bool:
        return Event.objects.prefetch_related(
            "members",
        ).get(id=event_id).members.filter(id=user_id).exists()

    @staticmethod
    @database_sync_to_async
    def get_messages_list(event_id: int) -> QuerySet:
        return Message.objects.select_related(
            "event",
            "user",
        ).filter(event_id=event_id).order_by("created_at")

    @staticmethod
    @database_sync_to_async
    def get_event_by_id(event_id: int) -> Event:
        return Event.objects.get(id=event_id)
