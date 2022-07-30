from rest_framework import serializers

from apps.users.serializers import UserSerializer

from . import models


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""

    count_members = serializers.SerializerMethodField(
        "get_count_members",
        read_only=True,
    )
    owner = UserSerializer(
        read_only=True,
    )

    def get_count_members(self, obj: models.Event) -> int:
        """Get count members of event."""
        return obj.members.count()

    class Meta:
        model = models.Event
        fields = (
            "id",
            "name",
            "description",
            "address",
            "datetime_spending",
            "is_online",
            "is_open",
            "owner",
            "count_members",
        )
