from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework import decorators, permissions, response, status

from apps.core.viewsets import BaseViewSet
from apps.events.filters import EventsFilter, filters
from apps.events.models import Event, Invite
from apps.events.permissions import EventMember, EventOwner
from apps.events.serializers import EventSerializer


class EventViewSet(BaseViewSet):
    """ViewSet for Event model."""

    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventsFilter
    permission_classes = (
        permissions.IsAuthenticated,
        EventMember | EventOwner,
    )

    def perform_create(self, serializer):
        """Custom save object."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Overriden for get queryset."""
        event = Event.objects.prefetch_related(
            "members",
        ).select_related("owner").order_by(
            "datetime_spending",
            "-is_finished",
        )
        if self.action == "list_events_user":
            return event.filter(owner=self.request.user)
        return event.filter(is_private=False)

    @decorators.action(methods=("GET",), detail=False, url_path="list-events")
    def list_events_user(self, request, *args, **kwargs):
        """Action for get list of events of user."""
        return super().list(request, *args, **kwargs)

    @decorators.action(methods=("POST",), detail=True, url_path="consist")
    def consist_in_event(self, request, pk: int = None) -> response.Response:
        """Action for enter/exit in event."""
        event = Event.objects.prefetch_related(
            Prefetch(
                "members",
                queryset=User.objects.filter(id=request.user.id),
            )
        ).get(id=pk)
        if event.is_private:
            return response.Response(
                data={"message": "You may not enter in event"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if request.user not in event.members.all():
            event.members.add(request.user)
        else:
            event.members.remove(request.user)
        return response.Response(
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=("PATCH",), detail=True, url_path="finish")
    def finish(self, request, pk: int = None) -> response.Response:
        """Action for finish event."""
        event = Event.objects.get(id=pk)
        event.is_finished = True
        event.save()
        invites = Invite.objects.filter(
            event_id=event.id,
            is_active=True,
        )
        for invite in invites:
            invite.is_active = False
            invite.save()
        return response.Response(
            data=EventSerializer(event).data,
            status=status.HTTP_200_OK,
        )
