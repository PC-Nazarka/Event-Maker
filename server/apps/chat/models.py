from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Message(models.Model):

    message = models.TextField(
        verbose_name=_("Message"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="messages",
        blank=True,
        null=True,
        verbose_name=_("Owner of message"),
    )
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("Event of message"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Datetime created message"),
    )
