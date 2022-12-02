from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EventsConfig(AppConfig):
    """Class-configuration of events app."""

    name = "apps.events"
    verbose_name = _("Events")

    def ready(self) -> None:
        import apps.events.signals  # noqa F401
