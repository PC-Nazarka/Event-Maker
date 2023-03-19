from django.contrib.auth.models import User

from apps.chat.models import Message
from apps.core.serializers import BaseModelSerializer, serializers
from apps.events.models import Event


class MessageSerializer(BaseModelSerializer):
    """Serializer for Message model."""

    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = Message
        fields = (
            "id",
            "message",
            "user",
            "event",
            "created_at",
        )
