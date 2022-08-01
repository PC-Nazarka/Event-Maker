import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.events.models import Event

from .. import factories

pytestmark = pytest.mark.django_db


def test_create_event(user, api_client) -> None:
    """Test create event."""
    event = factories.EventFactory.build(owner=user)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:events-list"),
        data={
            "name": event.name,
            "description": event.description,
            "address": event.address,
            "datetime_spending": event.datetime_spending,
            "is_online": event.is_online,
            "is_private": event.is_private,
            "is_finished": event.is_finished,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Event.objects.filter(
        name=event.name,
        description=event.description,
        address=event.address,
        datetime_spending=event.datetime_spending,
        is_online=event.is_online,
        is_private=event.is_private,
        is_finished=event.is_finished,
        owner=user,
    ).exists()


def test_update_event_by_owner(user, api_client) -> None:
    """Test update event by owner."""
    event = factories.EventFactory.create(owner=user)
    new_name = "New event"
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse_lazy("api:events-detail", kwargs={"pk": event.id}),
        data={
            "name": new_name,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert Event.objects.filter(
        name=new_name,
        description=event.description,
        address=event.address,
        datetime_spending=event.datetime_spending,
        is_online=event.is_online,
        is_private=event.is_private,
        is_finished=event.is_finished,
        owner=user,
    ).exists()


def test_update_event_by_member(user, api_client) -> None:
    """Test update event by member."""
    event = factories.EventFactory.create()
    event.members.add(user)
    new_name = "New event"
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse_lazy("api:events-detail", kwargs={"pk": event.id}),
        data={
            "name": new_name,
            "description": event.description,
            "address": event.address,
            "datetime_spending": event.datetime_spending,
            "is_online": event.is_online,
            "is_private": event.is_private,
            "is_finished": event.is_finished,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update_event_by_other_user(user, api_client) -> None:
    """Test update event by other user."""
    event = factories.EventFactory.create()
    new_name = "New event"
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse_lazy("api:events-detail", kwargs={"pk": event.id}),
        data={
            "name": new_name,
            "description": event.description,
            "address": event.address,
            "datetime_spending": event.datetime_spending,
            "is_online": event.is_online,
            "is_private": event.is_private,
            "is_finished": event.is_finished,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_event_by_owner(user, api_client) -> None:
    """Test delete event by owner."""


def test_delete_event_by_member(user, api_client) -> None:
    """Test delete event by member."""


def test_delete_event_by_other_user(user, api_client) -> None:
    """Test delete event by other user."""


def test_finish_event_by_owner(user, api_client) -> None:
    """Test finish event by owner."""


def test_finish_event_by_member(user, api_client) -> None:
    """Test finish event by member."""


def test_finish_event_by_other_user(user, api_client) -> None:
    """Test finish event by other user."""


def test_consists_in_event(user, api_client) -> None:
    """Test consist in event."""
