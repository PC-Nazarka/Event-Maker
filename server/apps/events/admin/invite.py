from django.contrib import admin

from apps.events.models import Invite


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    """Class representation of Invite model in admin panel."""

    autocomplete_fields = (
        "event",
        "user",
    )
    list_display = (
        "event",
        "user",
        "is_accepted",
        "is_active",
    )
