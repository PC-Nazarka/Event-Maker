from channels.db import database_sync_to_async
from django.contrib.auth.models import User
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
    def check_user_consist_in_event(user: User, event_id: int) -> bool:
        return (
            user in
            Event.objects.prefetch_related(
                "members"
            ).get(id=event_id).members.all()
        )

    @staticmethod
    @database_sync_to_async
    def get_messages_list(event_id: int) -> QuerySet:
        return Message.objects.select_related(
            "event",
            "user",
        ).filter(event__id=event_id).order_by("created_at")

    @staticmethod
    @database_sync_to_async
    def get_event_by_id(event_id: int) -> Event:
        return Event.objects.get(id=event_id)


class MessageQueries:

    @staticmethod
    @database_sync_to_async
    def create_message(data: dict) -> Message:
        return Message.objects.create(**data)

    @staticmethod
    @database_sync_to_async
    def check_message_owner(message_id: int, user_id: int) -> bool:
        return Message.objects.filter(
            id=message_id,
            user__id=user_id,
        ).exists()

    @staticmethod
    @database_sync_to_async
    def update_message(message_id: int, data: dict) -> None:
        Message.objects.filter(id=message_id).update(**data)

    @staticmethod
    @database_sync_to_async
    def get_message_by_id(message_id: int) -> Message:
        return Message.objects.get(id=message_id)

    @staticmethod
    @database_sync_to_async
    def delete_message(message_id: int) -> None:
        Message.objects.filter(id=message_id).delete()
