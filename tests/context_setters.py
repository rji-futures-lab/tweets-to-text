"""Context managers for setting global app context."""
from contextlib import contextmanager
from flask import appcontext_pushed, g


@contextmanager
def dynamodb_set(app, dynamodb_resource):
    """Add dynamodb_resource to the global app context."""
    def handler(sender, **kwargs):
        g.dynamodb = dynamodb_resource
    with appcontext_pushed.connected_to(handler, app):
        yield
