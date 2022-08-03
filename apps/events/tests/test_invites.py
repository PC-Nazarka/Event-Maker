import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.events import factories, models
from apps.users.factories import UserFactory

pytestmark = pytest.mark.django_db
INVITE_COUNT = 5


def test_create_invite(user, api_client) -> None:
    """Test create invite."""
    invite_user = UserFactory.create()
    event = factories.EventFactory.create(
        owner=user,
        is_finished=False,
    )
    invite = factories.InviteFactory.build(
        event=event,
        user=invite_user,
    )
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:invites-list"),
        data={
            "event": invite.event.pk,
            "user": invite.user.pk,
            "is_accepted": invite.is_accepted,
            "is_active": invite.is_active,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert models.Invite.objects.filter(
        event=invite.event,
        user=invite.user,
        is_accepted=invite.is_accepted,
        is_active=invite.is_active,
    ).exists()


def test_update_invite_by_owner(user, api_client) -> None:
    """Test update invite by owner."""
    event = factories.EventFactory.create(
        owner=user,
        is_finished=False,
    )
    invite = factories.InviteFactory.create(
        event=event,
        user=user,
    )
    is_accepted = not invite.is_accepted
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse_lazy("api:invites-detail", kwargs={"pk": invite.pk}),
        data={
            "is_accepted": is_accepted,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert models.Invite.objects.filter(
        event=invite.event,
        user=invite.user,
        is_accepted=is_accepted,
        is_active=invite.is_active,
    ).exists()


def test_update_invite_by_other_user(user, api_client) -> None:
    """Test update invite by other user."""
    invite = factories.InviteFactory.create()
    is_accepted = not invite.is_accepted
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse_lazy("api:invites-detail", kwargs={"pk": invite.pk}),
        data={
            "is_accepted": is_accepted,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_delete_invite_by_owner(user, api_client) -> None:
    """Test delete invite by owner."""
    event = factories.EventFactory.create(
        owner=user,
        is_finished=False,
    )
    invite = factories.InviteFactory.create(
        event=event,
        user=user,
    )
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse_lazy("api:invites-detail", kwargs={"pk": invite.pk}),
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not models.Invite.objects.filter(
        event=invite.event,
        user=invite.user,
        is_accepted=invite.is_accepted,
        is_active=invite.is_active,
    ).exists()


def test_delete_invite_by_other_user(user, api_client) -> None:
    """Test update invite by other user."""
    invite = factories.InviteFactory.create()
    api_client.force_authenticate(user=user)
    response = api_client.delete(
        reverse_lazy("api:invites-detail", kwargs={"pk": invite.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_accept_invite_true(user, api_client) -> None:
    """Test accept invite True."""
    event = factories.EventFactory.create()
    invite = factories.InviteFactory.create(
        event=event,
        user=user,
        is_active=True,
    )
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:invites-accept", kwargs={"pk": invite.pk}),
        data={
            "is_accepted": True,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert user in event.members.all()
    response = api_client.post(
        reverse_lazy("api:invites-accept", kwargs={"pk": invite.pk}),
        data={
            "is_accepted": True,
        },
    )
    assert str(response.data["is_accepted"][0]) == "Invite not active"
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert user in event.members.all()
    invite = factories.InviteFactory.create(
        event=event,
        user=user,
        is_active=True,
    )
    response = api_client.post(
        reverse_lazy("api:invites-accept", kwargs={"pk": invite.pk}),
        data={
            "is_accepted": True,
        },
    )
    assert (
        str(response.data["is_accepted"][0])
        == f"User {invite.user.username} is already member"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert user in event.members.all()


def test_accept_invite_false(user, api_client) -> None:
    """Test accept invite False."""
    event = factories.EventFactory.create()
    invite = factories.InviteFactory.create(
        event=event,
        user=user,
        is_active=True,
    )
    api_client.force_authenticate(user=user)
    response = api_client.post(
        reverse_lazy("api:invites-accept", kwargs={"pk": invite.pk}),
        data={
            "is_accepted": False,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert user not in event.members.all()
    response = api_client.post(
        reverse_lazy("api:invites-accept", kwargs={"pk": invite.pk}),
        data={
            "is_accepted": True,
        },
    )
    assert str(response.data["is_accepted"][0]) == "Invite not active"
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert user not in event.members.all()
    invite = factories.InviteFactory.create(
        event=event,
        user=user,
        is_active=True,
    )
    response = api_client.post(
        reverse_lazy("api:invites-accept", kwargs={"pk": invite.pk}),
        data={
            "is_accepted": True,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert user in event.members.all()
    invite = factories.InviteFactory.create(
        event=event,
        user=user,
        is_active=True,
    )
    response = api_client.post(
        reverse_lazy("api:invites-accept", kwargs={"pk": invite.pk}),
        data={
            "is_accepted": True,
        },
    )
    assert (
        str(response.data["is_accepted"][0])
        == f"User {invite.user.username} is already member"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert user in event.members.all()


def test_finish_event_and_not_active_invites(user, api_client) -> None:
    """Test set not active for invites of finish event."""
    event = factories.EventFactory.create(
        owner=user,
        is_finished=True,
    )
    factories.InviteFactory.create_batch(
        size=INVITE_COUNT,
        event=event,
        is_active=True,
    )
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        reverse_lazy("api:events-finish", kwargs={"pk": event.pk}),
    )
    assert response.status_code == status.HTTP_200_OK
    assert not all(
        [invite.is_active for invite in models.Invite.objects.filter(event=event)],
    )
