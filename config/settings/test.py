"""
With these settings, tests run faster.
"""

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="9HGHxyNgNi5QZdRqWIlteWuEFgZR6xrGrkQkFbabkfHm6EW6K9f9fzenAqgWAbSy",
)
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# PASSWORDS
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# DEBUGING FOR TEMPLATES
# ------------------------------------------------------------------------------
