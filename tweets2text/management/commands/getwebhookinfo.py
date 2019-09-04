"""Migrate data from DynamoDB into PostgreSQL."""
from django.core.management.base import BaseCommand
from tweets2text.twitter_api import TwitterMixin
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand, TwitterMixin):
    """Get info for current Twitter webhook."""

    help = "Get info for current Twitter webhook."

    def handle(self, *args, **options):
        """Handle the command."""
        response = self.twitter_api.request(
            'account_activity/all/webhooks'
        )

        response.response.raise_for_status()

        environments = response.json()['environments']

        if len(environments) > 0:
            for env in environments:
                self.stdout.write(
                    '  environment name: %s' % env['environment_name']
                )
                if len(env['webhooks']) < 1:
                    self.stdout.write(
                        self.style.WARNING('    No webhooks')
                    )
                else:
                    for wh in env['webhooks']:
                        for k, v in wh.items():
                            self.stdout.write('    %s: %s' % (k, v))
        else:
            self.stdout.write(
                self.style.WARNING('No environments')
            )
