from apps.core.serializers import BaseModelSerializer, serializers
from apps.events.models import Event
from apps.users.serializers import UserSerializer


class EventSerializer(BaseModelSerializer):
    """Serializer for Event model."""

    count_members = serializers.SerializerMethodField(
        "get_count_members",
        read_only=True,
    )
    owner = UserSerializer(
        read_only=True,
    )

    def get_count_members(self, obj: Event) -> int:
        """Get count members of event."""
        return obj.members.count()

    class Meta:
        model = Event
        fields = (
            "id",
            "name",
            "description",
            "address",
            "datetime_spending",
            "is_online",
            "is_private",
            "is_finished",
            "owner",
            "count_members",
        )
