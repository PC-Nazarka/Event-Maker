from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.core.viewsets import BaseViewSet
from apps.events.filters import InviteFilter, filters
from apps.events.models import Invite
from apps.events.permissions import InviteOwner
from apps.events.serializers import InviteAnswerSerializer, InviteSerializer


class InviteViewSet(BaseViewSet):
    """ViewSet for Invite model."""

    serializer_class = InviteSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InviteFilter
    permission_classes = (
        IsAuthenticated,
        InviteOwner,
    )

    def get_queryset(self):
        """Overriden for custom get queryset."""
        return Invite.objects.filter(
            user_id=self.request.user.id,
        )

    @action(methods=("POST",), detail=True, url_path="accept")
    def accept(self, request, pk: int = None) -> response.Response:
        """Action for accept or not accept invite."""
        serializer = InviteAnswerSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            status=status.HTTP_200_OK,
        )
