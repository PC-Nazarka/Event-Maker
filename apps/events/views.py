from rest_framework import response, status
from rest_framework.decorators import action

from apps.core.views import BaseViewSet

from . import models, serializers


class EventViewSet(BaseViewSet):
    """ViewSet for Event model."""

    queryset = models.Event.objects.filter(is_open=True)
    serializer_class = serializers.EventSerializer

    def perform_create(self, serializer):
        """Custom save object."""
        serializer.save(owner=self.request.user)

    @action(methods=("POST",), detail=True, url_path="enter")
    def enter_in_event(
        self,
        request,
        pk: int = None,
        *args,
        **kwargs,
    ) -> response.Response:
        """Action for enter in event."""
        event = models.Event.objects.get(id=pk)
        event.members.add(request.user)
        return response.Response(
            data=serializers.UserSerializer(
                event.members.all(),
                many=True,
            ).data,
            status=status.HTTP_202_ACCEPTED,
        )

    @action(methods=("POST",), detail=True, url_path="leave")
    def leave_from_event(
        self,
        request,
        pk: int = None,
        *args,
        **kwargs,
    ) -> response.Response:
        """Action for leave from event."""
        event = models.Event.objects.get(id=pk)
        event.members.remove(request.user)
        return response.Response(
            data=serializers.UserSerializer(
                event.members.all(),
                many=True,
            ).data,
            status=status.HTTP_202_ACCEPTED,
        )
