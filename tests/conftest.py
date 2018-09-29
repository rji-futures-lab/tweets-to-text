import pytest
from tweets2text import create_app


@pytest.fixture
def app():
    """
    Create and configure a new app instance for each test.
    """
    # create the app with common test config
    app = None
    app = create_app({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def incoming_follow():
    data = {
        "for_user_id": "1017142357932769280",
        "follow_events": [
            {
                "type": "follow",
                "created_timestamp": "1535652417571",
                "target": {
                    "id": "1017142357932769280",
                    "name": "TweetToText",
                },
                "source": {
                    "id": "1029178631921303553",
                    "name": "Bot2BotAction",  
                }
            }
        ]
    }

    return data


@pytest.fixture
def outgoing_follow():
    data = {
        "for_user_id": "1017142357932769280",
        "follow_events": [
            {
                "type": "follow",
                "created_timestamp": "1535652417571",
                "target": {
                    "id": "1029178631921303553",
                    "name": "Bot2BotAction",
                },
                "source": {
                    "id": "1017142357932769280",
                    "name": "TweetToText",
                }
            }
        ]
    }

    return data
