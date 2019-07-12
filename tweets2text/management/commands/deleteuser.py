"""Delete a user (and related records) from the db."""
from django.core.management.base import BaseCommand
from tweets2text.models import User
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand, TwitterMixin):
    """Delete a user (and related records) from the db."""

    help = """Delete a user (and related records) from the db."""

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):
        """Handle the command."""
        u = User.objects.get(id=options['user_id'])
        u.compilations.all().delete()
        u.follow_history.delete()
        u.delete()
