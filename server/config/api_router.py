from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.events.viewsets import EventViewSet, InviteViewSet
from apps.users.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="users")
router.register("events", EventViewSet, basename="events")
router.register("invites", InviteViewSet, basename="invites")

app_name = "api"
urlpatterns = router.urls