"""Migrate data from DynamoDB into PostgreSQL."""
import json
from django.core.management.base import BaseCommand
from tweets2text.twitter_api import TwitterMixin
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand, TwitterMixin):
    """Get info for current Twitter webhook."""

    help = "Get info for current Twitter webhook."

    def handle(self, *args, **options):
        """Handle the command."""
        response = self.twitter_api.request("account_activity/all/webhooks")

        response.response.raise_for_status()

        if self._called_from_command_line:
            info = json.dumps(
                response.json(), sort_keys=True, indent=4
            )
        else:
            info = response.text

        return info
