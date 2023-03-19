import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.events.factories import EventFactory
from apps.events.models import Event

pytestmark = pytest.mark.django_db


def test_create_event(user, api_client) -> None:
    """Test create event."""
    event = EventFactory.build(owner=user)
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
    event = EventFactory.create(
        owner=user,
        is_private=False,
        is_finished=False,
    )
    new_name = "New event"
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse_lazy("api:events-detail", kwargs={"pk": event.pk}),
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
    event = EventFactory.create(
        is_private=False,
        is_finished=False,
    )
    event.members.add(user)
    new_name = "New event"
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse_lazy("api:events-detail", kwargs={"pk": event.pk}),
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
    event = EventFactory.create(
        is_private=False,
        is_finished=False,
    )
    new_name = "New event"
    api_client.force_authenticate(user=user)
    response = api_client.put(
        reverse_lazy("api:events-detail", kwargs={"pk": event.pk}),
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
    event = EventFactory.create(
        owner=user,
        is_private=False,
        is_finished=False,
    )
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse_lazy("api:events-detail", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Event.objects.filter(
        name=event.name,
        description=event.description,
        address=event.address,
        datetime_spending=event.datetime_spending,
        is_online=event.is_online,
        is_private=event.is_private,
        is_finished=event.is_finished,
        owner=user,
    ).exists()


def test_delete_event_by_member(user, api_client) -> None:
    """Test delete event by member."""
    event = EventFactory.create(
        is_private=False,
        is_finished=False,
    )
    event.members.add(user)
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse_lazy("api:events-detail", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_event_by_other_user(user, api_client) -> None:
    """Test delete event by other user."""
    event = EventFactory.create(
        is_private=False,
        is_finished=False,
    )
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse_lazy("api:events-detail", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_finish_event_by_owner(user, api_client) -> None:
    """Test finish event by owner."""
    event = EventFactory.create(owner=user)
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse_lazy("api:events-finish", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_200_OK
    assert Event.objects.filter(
        name=event.name,
        description=event.description,
        address=event.address,
        datetime_spending=event.datetime_spending,
        is_online=event.is_online,
        is_private=event.is_private,
        is_finished=True,
        owner=user,
    ).exists()


def test_finish_event_by_member(user, api_client) -> None:
    """Test finish event by member."""
    event = EventFactory.create()
    event.members.add(user)
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse_lazy("api:events-finish", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_finish_event_by_other_user(user, api_client) -> None:
    """Test finish event by other user."""
    event = EventFactory.create()
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse_lazy("api:events-finish", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_consists_in_public_event(user, api_client) -> None:
    """Test consist in event."""
    event = EventFactory.create(
        is_private=False,
        is_finished=False,
    )
    api_client.force_authenticate(user=user)
    assert user not in event.members.all()
    response = api_client.post(
        reverse_lazy("api:events-consist-in-event", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_200_OK
    assert user in event.members.all()
    response = api_client.post(
        reverse_lazy("api:events-consist-in-event", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_200_OK
    assert user not in event.members.all()


def test_consists_in_private_event(user, api_client) -> None:
    """Test consist in private event."""
    event = EventFactory.create(
        is_private=True,
        is_finished=False,
    )
    api_client.force_authenticate(user=user)
    assert user not in event.members.all()
    response = api_client.post(
        reverse_lazy("api:events-consist-in-event", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert user not in event.members.all()
