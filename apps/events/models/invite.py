from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from .event import Event


class Invite(BaseModel):
    """Model of Invite."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        verbose_name=_("Event of invite"),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User of invite"),
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name=_("Accept user invite or not"),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active invite of not"),
    )
