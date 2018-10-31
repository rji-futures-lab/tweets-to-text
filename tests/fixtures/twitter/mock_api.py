"""Test fixtures mocking Twitter's API endpoints."""
import pytest


@pytest.fixture
def mock_direct_messages_new(app, requests_mock):
    """Mock Twitter's direct_messages/events/new endpoint."""
    return requests_mock.post(
        'https://api.twitter.com/1.1/direct_messages/events/new.json',
        json=dict()
    )


@pytest.fixture
def mock_statuses_update(app, requests_mock):
    """Mock Twitter's statuses/update endpoint."""
    return requests_mock.post(
        'https://api.twitter.com/1.1/statuses/update.json',
        json=dict()
    )


@pytest.fixture
def mock_statuses_user_timeline(app, requests_mock, tweet_set):
    """Mock Twitter's statuses/user_timeline endpoint."""
    return requests_mock.get(
        'https://api.twitter.com/1.1/statuses/user_timeline.json',
        json=tweet_set
    )
