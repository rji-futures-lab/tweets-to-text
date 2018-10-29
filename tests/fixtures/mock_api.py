"""Fixtures related to Twitter API."""
import pytest 

@pytest.fixture
def mock_direct_messages_new(app, requests_mock):
    return requests_mock.post(
        'https://api.twitter.com/1.1/direct_messages/events/new.json',
        json=dict()
    )


@pytest.fixture
def mock_statuses_update(app, requests_mock):
    return requests_mock.post(
        'https://api.twitter.com/1.1/statuses/update.json',
        json=dict()
    )

@pytest.fixture
def mock_statuses_user_timeline(app, requests_mock):
    return requests_mock.post(
        'https://api.twitter.com/1.1/statuses/user_timeline',
        json=dict()
    )
