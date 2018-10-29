"""Context managers for setting global app context."""
from contextlib import contextmanager
from flask import appcontext_pushed, g


@contextmanager
def dynamodb_set(app, dynamodb_client):
    """Add local dynamodb fixture to the global app context."""
    def handler(sender, **kwargs):
        g.dynamodb = dynamodb_client
    with appcontext_pushed.connected_to(handler, app):
        yield


@contextmanager
def s3_set(app, s3_client):
    """Add mock s3 fixture to the global app context."""
    def handler(sender, **kwargs):
        g.s3 = s3_client
    with appcontext_pushed.connected_to(handler, app):
        yield
