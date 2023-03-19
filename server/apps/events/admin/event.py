from django.contrib import admin

from apps.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Class representation of Event model in admin panel."""

    search_fields = (
        "name",
        "description",
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
