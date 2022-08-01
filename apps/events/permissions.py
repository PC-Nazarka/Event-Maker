from rest_framework import permissions


class EventMember(permissions.BasePermission):
    """Custom permission class for members of event."""

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in ("PUT", "PATCH", "DELETE"):
            return False
        return request.user in obj.members.all() if obj.is_private else True


class EventOwner(permissions.BasePermission):
    """Custom permission class for owner of event."""

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj.owner


class InviteOwner(permissions.BasePermission):
    """Custom permission class for invite for user."""

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user == obj.user
