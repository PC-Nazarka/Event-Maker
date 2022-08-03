from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.core.views import BaseViewSet, ListCreateUpdateDeleteViewSet

from . import models, permissions, serializers


class EventViewSet(BaseViewSet):
    """ViewSet for Event model."""

    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = (
        IsAuthenticated,
        permissions.EventMember | permissions.EventOwner,
    )

    def perform_create(self, serializer):
        """Custom save object."""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Overriden for get queryset."""
        queryset = self.queryset
        if self.action == "list_events_of_user":
            queryset = queryset.filter(
                user=self.request.user,
            )
        elif self.action == "list_events_main":
            queryset = queryset.filter(
                is_private=False,
                is_finished=False,
            )
        return queryset

    @action(methods=("GET",), detail=False, url_path="list-events")
    def list_events_user(self, request, *args, **kwargs):
        """Action for get list of events of user."""
        return super().list(request, *args, **kwargs)

    @action(methods=("GET",), detail=False, url_path="list-events")
    def list_events_main(self, request, *args, **kwargs):
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


class InviteViewSet(ListCreateUpdateDeleteViewSet):
    """ViewSet for Invite model."""

    queryset = models.Invite.objects.all()
    serializer_class = serializers.InviteSerializer
    permission_classes = (
        IsAuthenticated,
        permissions.InviteOwner,
    )

    def get_queryset(self):
        """Overriden for custom get queryset."""
        queryset = self.queryset
        if self.action == "list_invites":
            queryset = queryset.filter(user=self.request.user)
        return queryset

    @action(methods=("GET",), detail=False, url_path="users-invites")
    def list_invites(
        self,
        request,
        pk: int = None,
        *args,
        **kwargs,
    ) -> response.Response:
        """Action for get list of invites of current user."""
        return super().list(request, *args, **kwargs)

    @action(methods=("POST",), detail=True, url_path="accept")
    def accept(
        self,
        request,
        pk: int = None,
        *args,
        **kwargs,
    ) -> response.Response:
        """Action for accept or not accept invite."""
        serializer = serializers.InviteAnswerSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            status=status.HTTP_200_OK,
        )
