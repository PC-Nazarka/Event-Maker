from rest_framework import response, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.core.views import BaseViewSet

from .. import filters, models, permissions, serializers


class InviteViewSet(BaseViewSet):
    """ViewSet for Invite model."""

    serializer_class = serializers.InviteSerializer
    filter_backends = (filters.filters.DjangoFilterBackend,)
    filterset_class = filters.InviteFilter
    permission_classes = (
        IsAuthenticated,
        permissions.InviteOwner,
    )

    def get_queryset(self):
        """Overriden for custom get queryset."""
        return models.Invite.objects.select_related("user").filter(
            user=self.request.user,
        )

    @action(methods=("POST",), detail=True, url_path="accept")
    def accept(self, request, pk: int = None) -> response.Response:
        """Action for accept or not accept invite."""
        serializer = serializers.InviteAnswerSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            status=status.HTTP_200_OK,
        )
