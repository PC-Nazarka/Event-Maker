from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.events.views import EventViewSet, InviteViewSet
from apps.users.views import UserViewSet

app_name = "api"

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("events", EventViewSet, basename="events")
router.register("invites", InviteViewSet, basename="invites")

urlpatterns = router.urls
