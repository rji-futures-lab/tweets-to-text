"""Django settings when running project in test environment."""
from .local import * # noqa

THROTTLE_TWITTER_API_CALLS = False

LOGGING = {}
