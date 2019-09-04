"""Get a list of Twitter accounts the app is currently subscribed to."""
import json
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from tweets2text.twitter_api import TwitterMixin
from requests.exceptions import HTTPError
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand, TwitterMixin):
    """Get a list of Twitter accounts the app is currently subscribed to."""

    help = "Get a list of Twitter accounts the app is currently subscribed to."

    def handle(self, *args, **options):
        """Handle the command."""
        env = settings.TWITTER_API_ENV
        endpoint_url = f"account_activity/all/:{env}/subscriptions/list"
        response = self.twitter_api.request(endpoint_url)

        try:
            response.raise_for_status()
        except HTTPError:
            if 'errors' in response.json():
                self.write_stylized_response_items(
                    response.json()['errors'], error=True
                )
            raise CommandError(f" Status code: {response.status_code}")

        info = json.dumps(
            response.json(), sort_keys=True, indent=4
        )

        return info

    def write_stylized_response_items(self, items, error=False):
        """Write each in item to stdout with style."""
        for k, v in items:
            if error:
                msg = self.style.ERROR(f" {k}: {v}")
            else:
                msg = self.style.SUCCESS(f" {k}: {v}")
            self.stdout.write(msg)
