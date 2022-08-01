from django.contrib import admin

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    """Class representation of Event model in admin panel."""

    search_fields = (
        "name",
        "desctiption",
    )
    list_display = (
        "id",
        "name",
        "description",
        "address",
        "datetime_spending",
        "is_online",
        "is_private",
        "is_finished",
        "owner",
        "created",
        "modified",
    )


@admin.register(models.Invite)
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
