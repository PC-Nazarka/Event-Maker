from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.core.views import BaseViewSet

from .. import filters, models, permissions, serializers


class EventViewSet(BaseViewSet):
    """ViewSet for Event model."""

    queryset = models.Event.objects.filter(is_private=False, is_finished=False)
    serializer_class = serializers.EventSerializer
    filter_backends = (filters.filters.DjangoFilterBackend,)
    filterset_class = filters.EventsFilter
    permission_classes = (
        IsAuthenticated,
        permissions.EventMember | permissions.EventOwner,
    )

    def perform_create(self, serializer):
        """Custom save object."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Overriden for get queryset."""
        if self.action == "list_events_of_user":
            return models.Event.objects.filter(
                user=self.request.user,
            )
        return self.queryset

    @action(methods=("GET",), detail=False, url_path="list-events")
    def list_events_user(self, request, *args, **kwargs):
        """Action for get list of events of user."""
        return super().list(request, *args, **kwargs)

    @action(methods=("POST",), detail=True, url_path="consist")
    def consist_in_event(
        self,
        request,
        pk: int = None,
        *args,
        **kwargs,
    ) -> response.Response:
        """Action for enter/exit in event."""
        event = models.Event.objects.get(id=pk)
        if request.user not in event.members.all():
            event.members.add(request.user)
        else:
            event.members.remove(request.user)
        return response.Response(
            data=serializers.UserSerializer(
                event.members.all(),
                many=True,
            ).data,
            status=status.HTTP_202_ACCEPTED,
        )

    @action(methods=("PATCH",), detail=True, url_path="finish")
    def finish(
        self,
        request,
        pk: int = None,
        *args,
        **kwargs,
    ) -> response.Response:
        """Action for finish event."""
        event = models.Event.objects.get(id=pk)
        event.is_finished = True
        event.save()
        for invite in models.Invite.objects.filter(event=event):
            invite.is_active = False
            invite.save()
        return response.Response(
            data=serializers.EventSerializer(event).data,
            status=status.HTTP_200_OK,
        )
