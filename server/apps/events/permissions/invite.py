from rest_framework import permissions

from apps.events.models import Invite


class InviteOwner(permissions.BasePermission):
    """Custom permission class for invite for user."""

    def has_permission(self, request, view) -> bool:
        if request.method == "POST":
            if view.action == "accept":
                return (
                    Invite.objects.filter(
                        id=request.parser_context["kwargs"]["pk"],
                    ).first().user_id ==
                    request.user.id
                )
            return request.user.events_owner.filter(
                is_finished=False,
            ).exists()
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj.user
