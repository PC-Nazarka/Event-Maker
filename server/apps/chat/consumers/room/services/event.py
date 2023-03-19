from channels.db import database_sync_to_async
from django.db.models import QuerySet

from apps.chat.models import Message
from apps.chat.serializers import MessageSerializer
from apps.users.serializers import UserSerializer


class EventService:

    @staticmethod
    @database_sync_to_async
    def get_members_list(members: QuerySet) -> list:
        return UserSerializer(members, many=True).data

    @staticmethod
    @database_sync_to_async
    def get_messages_list(messages: QuerySet) -> list:
        return MessageSerializer(messages, many=True).data

    @staticmethod
    @database_sync_to_async
    def get_message(message: Message) -> list:
        return MessageSerializer(message).data
