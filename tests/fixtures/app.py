"""Fixtures related to app configuration."""
import pytest
from tweets2text import create_app
from tweets2text.dynamodb import schema


@pytest.fixture
def app(dynamodb):
    """Create and configure a new app instance for each test."""
    app = create_app({
        'TESTING': True,
    })

    for table_def in schema:
        dynamodb.create_table(**table_def)

    yield app
