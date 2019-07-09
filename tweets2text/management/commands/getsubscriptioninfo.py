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
            'account_activity/all/:{env}/subscriptions/list'.format(
                env=settings.TWITTER_API_ENV,
            )
        )

        if response.response.ok:
            for k, v in response.json():
                if type(v) == 'list':
                    self.stdout.write('  %s...' % k)
                    for i in v:
                        self.stdout.write('    %s' % v)
                else:
                    self.stdout.write('  %s: %s' % (k, v))
        else:
            if 'errors' in response.json():
                for e in response.json()['errors']:
                    for k, v in e.items():
                        self.stdout.write(
                            self.style.ERROR(' %s: %s' % (k, v))
                        )
            else:
                self.stdout.write(
                    self.style.ERROR(' Status code: %s' % response.status_code)
                )
