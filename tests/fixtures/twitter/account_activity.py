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
def audience_account():
    """Return account data (dict) for a Twitter user."""
    data = dict(
        id=1267635120,
        id_str='1267635120',
        name="Innovation & Futures Lab",
        screen_name='RJIFuturesLab',
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
def init_mention(user_account, bot_account):
    """Return tweet data (dict) with initial mention."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775808,
        id_str="1040981111734775808",
        text="Going live @TweetsToText",
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
                    screen_name=bot_account['screen_name'],
                    name=bot_account['name'],
                    id=bot_account['id'],
                    id_str=bot_account['id_str'],
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
        full_text="TweetsToText is a bot that lives on Twitter.",
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
        full_text="It collects your tweets into plain text files.",
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
        full_text="So you can take your brilliant observations somewhere else.",
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
def final_mention(user_account, bot_account):
    """Return tweet data (dict) with final mention."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775812,
        id_str="1040981111734775812",
        full_text="This bot was made in the RJI Futures Lab. @TweetsToText",
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
                    id=bot_account['id'],
                    id_str=bot_account['id_str'],
                    indices=[2, 15]
                )
            ],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def tweet_set(tweet1, tweet2, tweet3, final_mention):
    """Return tweet1, tweet2, tweet3 and final mention (list)."""
    return [tweet1, tweet2, tweet3, final_mention]


@pytest.fixture
def mention_by_bot(bot_account):
    """Return a tweet authored by the bot account."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775808,
        id_str="1040981111734775808",
        full_text="@TweetsToText",
        in_reply_to_status_id=None,
        in_reply_to_status_id_str=None,
        in_reply_to_user_id=None,
        in_reply_to_user_id_str=None,
        in_reply_to_screen_name=None,
        user=bot_account,
        is_quote_status=False,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[
                dict(
                    screen_name=bot_account['screen_name'],
                    name=bot_account['name'],
                    id=bot_account['id'],
                    id_str=bot_account['id_str'],
                    indices=[2, 15]
                )
            ],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def quote_tweet(user_account, bot_account):
    """Return tweet data (dict) with quote tweet."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775828,
        id_str="1040981111734775828",
        full_text="Going live w / @TweetsToText",
        in_reply_to_status_id=None,
        in_reply_to_status_id_str=None,
        in_reply_to_user_id=None,
        in_reply_to_user_id_str=None,
        in_reply_to_screen_name=None,
        user=user_account,
        is_quote_status=True,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[
                dict(
                    screen_name="TweetsToText",
                    name="TweetsToText",
                    id=bot_account['id'],
                    id_str=bot_account['id_str'],
                    indices=[2, 15]
                )
            ],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def self_reply_mention(user_account, bot_account, init_mention):
    """Return tweet data (dict) of user's self reply."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775818,
        id_str="1040981111734775818",
        full_text="That's a wrap @TweetsToText",
        in_reply_to_status_id=init_mention['id'],
        in_reply_to_status_id_str=init_mention['id_str'],
        in_reply_to_user_id=user_account['id'],
        in_reply_to_user_id_str=user_account['id_str'],
        in_reply_to_screen_name=user_account['screen_name'],
        user=user_account,
        is_quote_status=False,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[
                dict(
                    screen_name="TweetsToText",
                    name="TweetsToText",
                    id=bot_account['id'],
                    id_str=bot_account['id_str'],
                    indices=[2, 15]
                )
            ],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def non_self_reply_mention(user_account, bot_account, audience_account):
    """Return tweet data (dict) with reply mention."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775817,
        id_str="1040981111734775817",
        full_text="@Bot2BotAction @TweetsToText Go get em",
        in_reply_to_status_id=1040981111734775808,
        in_reply_to_status_id_str='1040981111734775808',
        in_reply_to_user_id=user_account['id'],
        in_reply_to_user_id_str=user_account['id_str'],
        in_reply_to_screen_name='Bot2BotAction',
        user=audience_account,
        is_quote_status=False,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[
                dict(
                    screen_name=bot_account['screen_name'],
                    name=bot_account['name'],
                    id=bot_account['id'],
                    id_str=bot_account['id_str'],
                    indices=[2, 15]
                ),
                dict(
                    screen_name=user_account['screen_name'],
                    name=user_account['name'],
                    id=user_account['id'],
                    id_str=user_account['id_str'],
                    indices=[2, 15]
                ),
            ],
            symbols=[]
        ),
        timestamp_ms="1537024212188",
    )
    return data


@pytest.fixture
def retweet(user_account, bot_account, init_mention):
    """Return data (dict) of the retweet of the initial mention."""
    data = dict(
        created_at="Sat Sep 15 15:10:12 +0000 2018",
        id=1040981111734775808,
        id_str="1040981111734775808",
        full_text="Going live w / @TweetsToText",
        in_reply_to_status_id=None,
        in_reply_to_status_id_str=None,
        in_reply_to_user_id=None,
        in_reply_to_user_id_str=None,
        in_reply_to_screen_name=None,
        user=user_account,
        is_quote_status=False,
        retweeted_status=init_mention,
        entities=dict(
            hashtags=[],
            urls=[],
            user_mentions=[
                dict(
                    screen_name="TweetsToText",
                    name="TweetsToText",
                    id=bot_account['id'],
                    id_str=bot_account['id_str'],
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
def mention_by_bot_activity(bot_account, mention_by_bot):
    """Return account activity data (dict) for mention by bot event."""
    data = dict(
        for_user_id=bot_account["id_str"],
    )
    return data


@pytest.fixture
def quote_tweet_activity(bot_account, quote_tweet):
    """Return account activity data (dict) for quote tweet event."""
    data = dict(
        for_user_id=bot_account["id_str"],
        tweet_create_events=[quote_tweet]
    )
    return data


@pytest.fixture
def self_reply_mention_activity(bot_account, self_reply_mention):
    """Return account activity data (dict) for self reply mention event."""
    data = dict(
        for_user_id=bot_account["id_str"],
        tweet_create_events=[self_reply_mention]
    )
    return data


@pytest.fixture
def non_self_reply_mention_activity(bot_account, non_self_reply_mention):
    """Return account activity data (dict) for reply from other user event."""
    data = dict(
        for_user_id=bot_account["id_str"],
        tweet_create_events=[non_self_reply_mention]
    )
    return data


@pytest.fixture
def retweet_activity(bot_account, retweet):
    """Return account activity data (dict) for retweet event."""
    data = dict(
        for_user_id=bot_account["id_str"],
        tweet_create_events=[retweet]
    )
    return data
