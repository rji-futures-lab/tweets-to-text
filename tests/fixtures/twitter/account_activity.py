"""Twitter account activity test fixtures."""
import pytest


@pytest.fixture
def bot_account():
    """Return account data (dict) for TweetsToText bot."""
    data = dict(
        id=1017142357932769280,
        id_str='1017142357932769280',
        name="TweetsToText",
        screen_name='TweetsToText',
    )
    return data


@pytest.fixture
def user_account():
    """Return account data (dict) for a Twitter user."""
    data = dict(
        id=1029178631921303553,
        id_str='1029178631921303553',
        name="Bot2BotAction",
        screen_name='Bot2BotAction',
    )
    return data


@pytest.fixture
def incoming_follow_activity(bot_account, user_account):
    """Return account activity data (dict) for incoming follow event."""
    data = dict(
        for_user_id=bot_account["id_str"],
        follow_events=[
            dict(
                type="follow",
                created_timestamp="1535652417571",
                target=bot_account,
                source=user_account,
            )
        ]
    )
    return data


@pytest.fixture
def outgoing_follow_activity(bot_account, user_account):
    """Return account activity data (dict) for outgoing follow event."""
    data = dict(
        for_user_id=bot_account["id_str"],
        follow_events=[
            dict(
                type="follow",
                created_timestamp="1535652417571",
                target=user_account,
                source=bot_account,
            )
        ]
    )
    return data


@pytest.fixture
def init_mention(user_account):
    """Return tweet data (dict) with initial mention."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775808,
        id_str="1040981111734775808",
        text="Going live w / @TweetsToText",
        in_reply_to_status_id=None,
        in_reply_to_status_id_str=None,
        in_reply_to_user_id=None,
        in_reply_to_user_id_str=None,
        in_reply_to_screen_name=None,
        user=user_account,
        is_quote_status=False,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[
                dict(
                    screen_name="TweetsToText",
                    name="TweetsToText",
                    id=user_account['id'],
                    id_str=user_account['id_str'],
                    indices=[2, 15]
                )
            ],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def tweet1(user_account):
    """Return tweet data (dict) for first tweet."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775809,
        id_str="1040981111734775809",
        text="TweetsToText is a bot that lives on Twitter.",
        in_reply_to_status_id=None,
        in_reply_to_status_id_str=None,
        in_reply_to_user_id=None,
        in_reply_to_user_id_str=None,
        in_reply_to_screen_name=None,
        user=user_account,
        is_quote_status=False,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def tweet2(user_account):
    """Return tweet data (dict) for second tweet."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775810,
        id_str="1040981111734775810",
        text="It collects your tweets into plain text files.",
        in_reply_to_status_id=None,
        in_reply_to_status_id_str=None,
        in_reply_to_user_id=None,
        in_reply_to_user_id_str=None,
        in_reply_to_screen_name=None,
        user=user_account,
        is_quote_status=False,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def tweet3(user_account):
    """Return tweet data (dict) for third tweet."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775811,
        id_str="1040981111734775811",
        text="So you can take your brilliant observations somewhere else.",
        in_reply_to_status_id=None,
        in_reply_to_status_id_str=None,
        in_reply_to_user_id=None,
        in_reply_to_user_id_str=None,
        in_reply_to_screen_name=None,
        user=user_account,
        is_quote_status=False,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def final_mention(user_account):
    """Return tweet data (dict) with final mention."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775812,
        id_str="1040981111734775812",
        text="This bot was made in the RJI Futures Lab. @TweetsToText",
        in_reply_to_status_id=None,
        in_reply_to_status_id_str=None,
        in_reply_to_user_id=None,
        in_reply_to_user_id_str=None,
        in_reply_to_screen_name=None,
        user=user_account,
        is_quote_status=False,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[
                dict(
                    screen_name="TweetsToText",
                    name="TweetsToText",
                    id=user_account['id'],
                    id_str=user_account['id_str'],
                    indices=[2, 15]
                )
            ],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def init_mention_activity(bot_account, init_mention):
    """Return account activity data (dict) for initial mention event."""
    data = dict(
        for_user_id=bot_account["id_str"],
        tweet_create_events=[init_mention]
    )
    return data


@pytest.fixture
def final_mention_activity(bot_account, final_mention):
    """Return account activity data (dict) for final mention event."""
    data = dict(
        for_user_id=bot_account["id_str"],
        tweet_create_events=[final_mention]
    )
    return data


@pytest.fixture
def tweet_set(tweet1, tweet2, tweet3, final_mention):
    """Return tweet1, tweet2, tweet3 and final mention (list)."""
    return [tweet1, tweet2, tweet3, final_mention]
