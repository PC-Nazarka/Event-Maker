from django.contrib.auth.models import User

from apps.core.serializers import BaseModelSerializer, serializers
from apps.events.models import Event

from . import models


class MessageSerializer(BaseModelSerializer):
    """Serializer for Message model."""

    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = models.Message
        fields = (
            "id",
            "message",
            "user",
            "event",
            "created_at",
        )
