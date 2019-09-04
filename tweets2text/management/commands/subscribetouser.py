"""Subscribe to the bot account's activity."""
from django.conf import settings
from django.core.management.base import BaseCommand
from tweets2text.twitter_api import TwitterMixin
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand, TwitterMixin):
    """Subscribe to the bot account's activity."""

    help = """Subscribe to the bot account's activity."""

    def handle(self, *args, **options):
        """Handle the command."""
        env = settings.TWITTER_API_ENV
        endpoint_url = f"account_activity/all/:{env}/subscriptions"

        response = self.twitter_api.request(
            endpoint_url, method_override='POST'
        )

        if response.status_code == 204:
            msg = self.style.SUCCESS(" Subscribed to user.")
        else:
            msg = self.style.ERROR(f" Status code: {response.status_code}")

        return msg
