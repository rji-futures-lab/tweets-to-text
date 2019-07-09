"""Migrate data from DynamoDB into PostgreSQL."""
from django.conf import settings
from django.core.management.base import BaseCommand
from tweets2text.twitter_api import TwitterMixin
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand, TwitterMixin):
    """Get info for current Twitter webhook."""

    help = """Get info for current Twitter webhook."""

    def handle(self, *args, **options):
        """Handle the command."""
        response = self.twitter_api.request(
            'account_activity/all/:{}/subscriptions'.format(
                settings.TWITTER_API_ENV,
            ),
            method_override='POST'
        )
        if response.status_code == 204:
            self.stdout.write(self.style.SUCCESS(' Subscribed to user.'))
        else:
            self.stdout.write(
                self.style.ERROR(' Status code: %s' % response.status_code)
            )
