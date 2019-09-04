"""Replace current webhook url with new one under domain provided by user."""
import json
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Replace current webhook url with new one under domain provided by user.

    Delete the current webhook, then register a new one and subscribe to the
    bot account.
    """

    help = (
        "Replace current webhook url with new one under domain provided by user. " # noqa
        "Delete the current webhook, then register a new one and subscribe to "
        "bot account."
    )

    def add_arguments(self, parser):
        parser.add_argument('domain', type=str)

    def handle(self, *args, **options):
        """Handle the command."""
        site = Site.objects.get_current()
        old_domain = site.domain
        site.domain = options['domain']
        site.save()
        self.stdout.write(f" Replaced {old_domain} with {site.domain}.")

        webhook = self.get_current_webhook()
        if webhook:
            call_command('deletewebhook', webhook['id'])

        call_command('registerwebhook')
        call_command('subscribetouser')

        return self.style.SUCCESS(f'Finished.')

    def get_current_webhook(self):
        webhook_info = json.loads(call_command('getwebhookinfo'))
        environments_by_name = {
            e['environment_name']: e for e in webhook_info['environments']
        }
        current_env = environments_by_name[settings.TWITTER_API_ENV]
        sorted_webhooks = sorted(
            current_env['webhooks'],
            key=lambda i: i['created_timestamp'],
            reverse=True
        )
        try:
            current_webhook = sorted_webhooks[0]
        except IndexError:
            return None
        else:
            return current_webhook
