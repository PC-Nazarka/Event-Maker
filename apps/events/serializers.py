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


class InviteAnswerSerializer(serializers.Serializer):
    """Serializer for answer of invite."""

    is_accepted = serializers.BooleanField()

    def validate_is_accepted(self, is_accepted: bool) -> bool:
        """Method for validate is_accepted field."""
        self.invite = models.Invite.objects.filter(
            id=self.context["request"].parser_context["kwargs"]["pk"],
        ).first()
        if not self.invite.is_active:
            raise serializers.ValidationError(
                "Invite not active",
            )
        if self.invite.user in self.invite.event.members.all() and is_accepted:
            raise serializers.ValidationError(
                f"User {self.invite.user.username} is already member",
            )
        return is_accepted

    def save(self) -> None:
        """Overriden for change invite."""
        is_accepted = self.validated_data["is_accepted"]
        self.invite.is_accepted = is_accepted
        if is_accepted:
            self.invite.event.members.add(self.invite.user)
        self.invite.is_active = False
        self.invite.save()
