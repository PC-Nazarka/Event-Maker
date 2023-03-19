from channels.db import database_sync_to_async

from apps.chat.models import Message


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
            user_id=user_id,
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
