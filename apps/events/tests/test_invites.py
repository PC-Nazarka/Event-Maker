import pytest
from django.urls import reverse_lazy
from rest_framework import status

from apps.events.models import Invite

from .. import factories
