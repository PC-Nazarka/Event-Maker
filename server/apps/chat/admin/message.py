from django.contrib import admin

from apps.chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Class representation of Message model in admin panel."""

    list_display = (
        "id",
        "message",
        "user",
        "event",
        "created_at",
    )
