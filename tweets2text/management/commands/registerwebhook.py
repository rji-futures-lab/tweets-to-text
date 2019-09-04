"""Register a webhook url for the current domain."""
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError
from requests.exceptions import HTTPError
from tweets2text.twitter_api import TwitterMixin
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand, TwitterMixin):
    """
    Register a webhook url for the current domain.

    Sends a POST request to the webhooks endpoint of Twitter's Account Activity
    API. This triggers a CRC request from Twitter to the app's webhook url.
    """

    help = (
        "Register a webhook url for the current domain.\n",
        "Sends a POST request to the webhooks endpoint of Twitter's Account "
        "Activity API. This triggers a CRC request from Twitter to the app's "
        "webhook url."
    )

    def handle(self, *args, **options):
        """Handle the command."""
        domain = Site.objects.get_current().domain
        webhook_url = f"https://{domain}/webhooks/twitter/"

        self.stdout.write(f" Registering {webhook_url}...")

        endpoint = f"account_activity/all/:{settings.TWITTER_API_ENV}/webhooks"

        response = self.twitter_api.request(
            endpoint, params={'url': webhook_url}
        )

        try:
            response.raise_for_status()
        except HTTPError:
            if 'errors' in response.json():
                for e in response.json()['errors']:
                    self.write_stylized_response_items(e.items(), error=True)
            raise CommandError(f" Status code: {response.status_code}")
        else:
            self.write_stylized_response_items(response.json().items())

    def write_stylized_response_items(self, items, error=False):
        """Write each in item to stdout with style."""
        for k, v in items:
            if error:
                msg = self.style.ERROR(f" {k}: {v}")
            else:
                msg = self.style.SUCCESS(f" {k}: {v}")
            self.stdout.write(msg)
