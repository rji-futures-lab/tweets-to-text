"""
Tests written in pytest style.
"""
import pytest
from pytest_dynamodb import factories
from tweets2text import create_app
from tweets2text.dynamodb import schema


@pytest.fixture
def app(dynamodb):
    """
    Create and configure a new app instance for each test.
    """
    app = create_app({
        'TESTING': True,
    })

    for table_def in schema:
        dynamodb.create_table(**table_def)

    yield app


@pytest.fixture
def incoming_follow_data():
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
def outgoing_follow_data():
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


@pytest.fixture
def mock_friendships_create(app, requests_mock):
    return requests_mock.post(
        'https://api.twitter.com/1.1/friendships/create.json',
        json=dict()
    )



# @pytest.fixture
# def incoming_follow_event(app, incoming_follow_data, requests_mock):
#     # with dynamodb_set(app):
#     requests_mock.post(
#         'https://api.twitter.com/1.1/friendships/create.json',
#         json=dict()
#     )
#     with app.test_client() as c:
#         response = c.post(
#             '/webhooks/twitter/',
#             json=incoming_follow_data
#         )
#     return response


# @pytest.fixture
# def outgoing_follow_event(app, outgoing_follow_data):
#     # with dynamodb_set(app):
#     with app.test_client() as c:
#         response = c.post(
#             '/webhooks/twitter/',
#             json=outgoing_follow_data
#         )
#     return response
