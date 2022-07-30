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
        "is_open",
        "owner",
        "created",
        "modified",
    )
