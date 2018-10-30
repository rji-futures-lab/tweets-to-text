"""Fixtures related to app configuration."""
import os
import json
import boto3
from moto.s3 import mock_s3
import pytest
from tweets2text import create_app
from tweets2text.dynamodb import schema
from tests.context_setters import dynamodb_set


@pytest.fixture
def s3():
    """Yield a mock AWS S3 client."""
    with mock_s3():
        s3 = boto3.client('s3')
        yield s3


@pytest.fixture
def dynamodb_w_pending_job(app, dynamodb, init_mention):
    """Yield a mock AWS DynamoDb client with a pending job."""
    with dynamodb_set(app, dynamodb):
        job = dict(
            user_id=init_mention['user']['id'],
            init_tweet_id=init_mention['id'],
            screen_name=init_mention['user']['screen_name'],
            init_event_json=json.dumps(init_mention)
        )
        dynamodb.Table('TweetsToText-jobs').put_item(Item=job)
        yield dynamodb


@pytest.fixture
def app(dynamodb, s3):
    """Yield a configured new app instance for each test."""
    app = create_app({
        'TESTING': True,
    })

    for table_def in schema:
        dynamodb.create_table(**table_def)

    s3.create_bucket(Bucket='test-tweets-to-text-downloads')

    yield app
