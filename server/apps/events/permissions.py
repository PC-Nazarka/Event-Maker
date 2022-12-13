from rest_framework import permissions

from . import models


class EventMember(permissions.BasePermission):
    """Custom permission class for members of event."""

    def has_permission(self, request, view) -> bool:
        return view.action != "finish"

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PUT", "PATCH", "DELETE"):
            return False
        return request.user in obj.members.all() if obj.is_private else True


class EventOwner(permissions.BasePermission):
    """Custom permission class for owner of event."""

    def has_permission(self, request, view) -> bool:
        return (
            models.Event.objects.select_related("owner").filter(
                id=request.parser_context["kwargs"]["pk"],
            ).first().owner ==
            request.user
        )

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj.owner


class InviteOwner(permissions.BasePermission):
    """Custom permission class for invite for user."""

    def has_permission(self, request, view) -> bool:
        if request.method == "POST":
            if view.action == "accept":
                return (
                    models.Invite.objects.select_related("user").filter(
                        id=request.parser_context["kwargs"]["pk"],
                    ).first().user ==
                    request.user
                )
            return request.user.events_owner.filter(
                is_finished=False,
            ).exists()
        return True

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj.user
