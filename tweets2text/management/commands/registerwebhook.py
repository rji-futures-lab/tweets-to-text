"""Register a webhook url for the current domain."""
from urllib.parse import urljoin
from django.conf import settings
from django.core.management.base import BaseCommand
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

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)

    def handle(self, *args, **options):
        """Handle the command."""
        url = urljoin(options['domain'], 'webhooks/twitter/')

        self.stdout.write(' Registering %s...' % url)

        response = self.twitter_api.request(
            'account_activity/all/:%s/webhooks' % settings.TWITTER_API_ENV,
            params={'url': url},
        )

        if response.response.ok:
            for k, v in response.json().items():
                self.stdout.write(
                    self.style.SUCCESS(' %s: %s' % (k, v))
                )
        else:
            if 'errors' in response.json():
                for e in response.json()['errors']:
                    for k, v in e.items():
                        self.stdout.write(
                            self.style.ERROR(' %s: %s' % (k, v))
                        )
            else:
                self.stdout.write(
                    self.style.ERROR('Status')
                )
