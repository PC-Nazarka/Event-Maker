from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models, tasks


@receiver(post_save, sender=models.Invite)
def send_email_about_invite(instance, created, **kwargs) -> None:
    """Signal when invite created."""
    if created:
        tasks.send_email_invite.delay(instance.id)
