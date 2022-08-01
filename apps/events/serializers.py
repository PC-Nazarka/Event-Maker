from apps.core.serializers import BaseModelSerializer, serializers
from apps.users.serializers import User, UserSerializer

from . import models


class EventSerializer(BaseModelSerializer):
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
            "is_private",
            "is_finished",
            "owner",
            "count_members",
        )


class InviteSerializer(BaseModelSerializer):
    """Serializer for Invite model."""

    event = serializers.PrimaryKeyRelatedField(
        queryset=models.Event.objects.all(),
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = models.Invite
        fields = (
            "id",
            "event",
            "user",
            "is_accepted",
            "is_active",
        )

    def validate_user(self, user: User) -> User:
        """Method for validate user field."""
        event = models.Event.objects.get(id=self._request.data["event"])
        if user in event.members.all():
            raise serializers.ValidationError(
                f"User {user.username} is already member.",
            )
        return user
