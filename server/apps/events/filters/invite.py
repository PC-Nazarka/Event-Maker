from django_filters import rest_framework as filters

from apps.events.models import Invite


class InviteFilter(filters.FilterSet):
    """
    Filter for invite.

    Filter by:
        is_accepted
    """

    is_accepted = filters.BooleanFilter(
        field_name="is_accepted",
    )

    class Meta:
        model = Invite
        fields = (
            "is_accepted",
        )
