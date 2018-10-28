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
def init_mention():
    data = {
        "for_user_id": "1017142357932769280",
        "tweet_create_events": [
            {
                "created_at": "Sat Sep 15 15:10:12 +0000 2018",
                "id": 1040981111734775808,
                "id_str": "1040981111734775808",
                "text": "Going live w / @TweetsToText",
                "truncated": False,
                "in_reply_to_status_id": None,
                "in_reply_to_status_id_str": None,
                "in_reply_to_user_id": None,
                "in_reply_to_user_id_str": None,
                "in_reply_to_screen_name": None,
                "user": {
                    "id": 258415976,
                    "id_str": "258415976",
                    "name": "James Gordon",
                    "screen_name": "JE_Gordon",
                    "location": "Columbia, MO",
                    "utc_offset": None,
                    "time_zone": None,
                    "geo_enabled": False,
                    "lang": "en",
                    "is_translator": False,
                    "following": None,
                    "follow_request_sent": None,
                    "notifications": None
                },
                "geo": None,
                "coordinates": None,
                "place": None,
                "contributors": None,
                "is_quote_status": False,
                "quote_count": 0,
                "reply_count": 0,
                "retweet_count": 0,
                "favorite_count": 0,
                "entities": {
                    "hashtags": [],
                    "urls": [],
                    "user_mentions": [
                        {
                            "screen_name": "TweetsToText",
                            "name": "TweetToText",
                            "id": 1017142357932769280,
                            "id_str": "1017142357932769280",
                            "indices": [2, 15]
                        }
                    ],
                    "symbols": []
                },
                "favorited": False,
                "retweeted": False,
                "filter_level": "low",
                "lang": "und",
                "timestamp_ms": "1537024212188"
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

@pytest.fixture
def mock_statuses_update(app, requests_mock):
    return requests_mock.post(
        'https://api.twitter.com/1.1/statuses/update.json',
        json=dict()
    )
