"""Fixtures related to app configuration."""
import json
import boto3
from moto.s3 import mock_s3
import pytest
from tweets2text import create_app
from tweets2text.dynamodb import schema
from tests.context_setters import dynamodb_set


@pytest.fixture
def moto_s3():
    """Yield a mock AWS S3 resources."""
    with mock_s3():
        s3 = boto3.resource('s3')
        yield s3


@pytest.fixture
def s3_bucket(moto_s3):
    """Create and return a mock S3 bucket."""
    bucket = moto_s3.Bucket('test-tweets-to-text-downloads')
    bucket.create()
    return bucket


@pytest.fixture
def dynamodb_w_pending_job(app, dynamodb, init_mention):
    """Yield a mock AWS DynamoDb resource with a pending job."""
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
def app(dynamodb):
    """Yield a configured new app instance for each test."""
    app = create_app({
        'TESTING': True,
    })

    for table_def in schema:
        dynamodb.create_table(**table_def)

    yield app
