from django_filters import rest_framework as filters

from .. import models


class EventsFilter(filters.FilterSet):
    """
    Filter for event.

    Filter by:
        name
        description
        address
        datetime_spending
        is_online
    """

    name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
    )
    description = filters.CharFilter(
        field_name="description",
        lookup_expr="icontains",
    )
    address = filters.CharFilter(
        field_name="address",
        lookup_expr="icontains",
    )
    start_date = filters.DateFilter(
        field_name="datetime_spending",
        lookup_expr="date__gt",
    )
    end_date = filters.DateFilter(
        field_name="datetime_spending",
        lookup_expr="date__lt",
    )
    is_online = filters.BooleanFilter(
        field_name="is_online",
    )

    class Meta:
        model = models.Event
        fields = (
            "name",
            "description",
            "address",
            "datetime_spending",
            "is_online",
        )
