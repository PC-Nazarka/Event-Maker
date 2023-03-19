from django.contrib.auth.models import User

from apps.core.serializers import BaseModelSerializer, serializers
from apps.events.models import Event, Invite


class InviteSerializer(BaseModelSerializer):
    """Serializer for Invite model."""

    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(),
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = Invite
        fields = (
            "id",
            "event",
            "user",
            "is_accepted",
            "is_active",
        )

    def validate_user(self, user: User) -> User:
        """Method for validate user field."""
        is_exists = Event.objects.prefetch_related(
            "members",
        ).get(
            id=self._request.data["event"],
        ).members.filter(id=user.id).exists()
        if is_exists:
            raise serializers.ValidationError(
                f"User {user.username} is already member.",
            )
        return user


class InviteAnswerSerializer(serializers.Serializer):
    """Serializer for answer of invite."""

    is_accepted = serializers.BooleanField()

    def validate_is_accepted(self, is_accepted: bool) -> bool:
        """Method for validate is_accepted field."""
        self.invite = Invite.objects.select_related(
            "event",
            "user",
        ).prefetch_related(
            "event__members",
        ).filter(
            id=self.context["request"].parser_context["kwargs"]["pk"],
        ).first()
        if self.invite.event.is_finished:
            raise serializers.ValidationError(
                "Event is finished",
            )
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
