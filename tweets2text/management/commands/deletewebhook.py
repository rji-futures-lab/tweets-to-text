"""Delete the current webhook with Twitter."""
from django.conf import settings
from django.core.management.base import BaseCommand
from tweets2text.twitter_api import TwitterMixin
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand, TwitterMixin):
    """
    Delete the current webhook with Twitter.

    Sends a DELETE request to the webhooks endpoint of the Twitter Account
    Activity API.
    """

    help = (
        "Delete the current webhook with Twitter.\n"
        "Sends a DELETE request to the webhooks endpoint of the Twitter "
        "Account Activity API."
    )

    def add_arguments(self, parser):
        parser.add_argument('webhook_id', type=str)

    def handle(self, *args, **options):
        """Handle the command."""
        env = settings.TWITTER_API_ENV
        webhook_id = options['webhook_id']

        endpoint_url = f"account_activity/all/:{env}/webhooks/:{webhook_id}"

        response = self.twitter_api.request(
            endpoint_url, method_override='DELETE'
        )

        if response.status_code == 204:
            msg = self.style.SUCCESS("Webhook deleted.")
        else:
            msg = self.style.ERROR(f" Status code: {response.status_code}")

        return msg
