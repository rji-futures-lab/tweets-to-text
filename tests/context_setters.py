"""Context managers for setting global app context."""
from contextlib import contextmanager
from flask import appcontext_pushed, g


@contextmanager
def aws_resources_set(app, dynamodb_resource, s3_bucket):
    """Add dynamodb_resource and s3_bucket to the global app context."""
    def handler(sender, **kwargs):
        g.dynamodb = dynamodb_resource
        g.s3_bucket = s3_bucket
    with appcontext_pushed.connected_to(handler, app):
        yield


@contextmanager
def dynamodb_set(app, dynamodb_resource):
    """Add dynamodb_resource to the global app context."""
    def handler(sender, **kwargs):
        g.dynamodb = dynamodb_resource
    with appcontext_pushed.connected_to(handler, app):
        yield
