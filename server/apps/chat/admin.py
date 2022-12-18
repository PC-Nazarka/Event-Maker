from django.contrib import admin

from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
    """Class representation of Message model in admin panel."""

    list_display = (
        "id",
        "message",
        "user",
        "event",
        "created_at",
    )
