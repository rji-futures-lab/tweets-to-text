from django.conf import settings

bot = dict(
    id=int(settings.BOT_ACCOUNT_ID_STR),
    id_str=settings.BOT_ACCOUNT_ID_STR,
    name="TweetsToText",
    screen_name='TweetsToText',
)

user = dict(
    id=1029178631921303553,
    id_str='1029178631921303553',
    name="Bot2BotAction",
    screen_name='Bot2BotAction',
    location='Anytown, USA'
)

user2 = dict(
    id=1267635120,
    id_str='1267635120',
    name="RJI Futures Lab",
    screen_name='RJIFuturesLab',
    location='Columbia, Mo'
)

follow_event = dict(
    type='follow',
    created_timestamp="1517588749178",
    target=bot,
    source=user,
)

unfollow_event = dict(
    type='unfollow',
    created_timestamp="1517588749178",
    target=bot,
    source=user,
)

bot_follow_event = dict(
    type='follow',
    created_timestamp="1517588749178",
    target=user,
    source=bot,
)

init_mention = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775808,
    id_str="1040981111734775808",
    text="Going live @TweetsToText",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            dict(
                screen_name=bot['screen_name'],
                name=bot['name'],
                id=bot['id'],
                id_str=bot['id_str'],
                indices=[2, 15]
            )
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

init_mention_w_full_text = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775808,
    id_str="1040981111734775808",
    full_text="Going live @TweetsToText",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            dict(
                screen_name=bot['screen_name'],
                name=bot['name'],
                id=bot['id'],
                id_str=bot['id_str'],
                indices=[2, 15]
            )
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

init_tweet_no_mention = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775808,
    id_str="1040981111734775808",
    text="Going live",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            dict(
                screen_name=bot['screen_name'],
                name=bot['name'],
                id=bot['id'],
                id_str=bot['id_str'],
                indices=[2, 15]
            )
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

init_tweet_no_mention_full_text = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775808,
    id_str="1040981111734775808",
    full_text="Going live",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            dict(
                screen_name=bot['screen_name'],
                name=bot['name'],
                id=bot['id'],
                id_str=bot['id_str'],
                indices=[2, 15]
            )
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)


quoted_mention = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775808,
    id_str="1040981111734775808",
    text="Going live @TweetsToText",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=True,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            dict(
                screen_name=bot['screen_name'],
                name=bot['name'],
                id=bot['id'],
                id_str=bot['id_str'],
                indices=[2, 15]
            )
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

reply_mention = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775809,
    id_str="1040981111734775809",
    text="Going live @TweetsToText",
    in_reply_to_status_id=1040981111734775808,
    in_reply_to_status_id_str="1040981111734775808",
    in_reply_to_user_id=user['id'],
    in_reply_to_user_id_str=user['id_str'],
    in_reply_to_screen_name=user['screen_name'],
    user=user2,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            dict(
                screen_name=bot['screen_name'],
                name=bot['name'],
                id=bot['id'],
                id_str=bot['id_str'],
                indices=[2, 15]
            )
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

retweet_mention = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775808,
    id_str="1040981111734775808",
    text="Going live @TweetsToText",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user2,
    is_quote_status=False,
    retweeted_status=init_mention,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            dict(
                screen_name=bot['screen_name'],
                name=bot['name'],
                id=bot['id'],
                id_str=bot['id_str'],
                indices=[2, 15]
            )
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

tweet1 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775809,
    id_str="1040981111734775809",
    full_text="TweetsToText is a bot that lives on Twitter.",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

tweet2 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775810,
    id_str="1040981111734775810",
    full_text="It collects your tweets into plain text files.",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

tweet3 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775811,
    id_str="1040981111734775811",
    full_text="So you can take your brilliant observations somewhere else.",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

tweet4 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775812,
    id_str="1040981111734775812",
    full_text="This bot was made in the @%s." % user2['screen_name'],
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            user2,
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

tweet5 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775813,
    id_str="1040981111734775813",
    full_text="You can find out more here: https://t.co/1YJGc8kavu.",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[
            dict(
                url='https://t.co/1YJGc8kavu',
                expanded_url="https://www.tweetstotext.io"
            ),
        ],
        user_mentions=[],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

final_mention = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775814,
    id_str="1040981111734775814",
    full_text="Thank you, that is all. @TweetsToText",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            bot,
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

final_tweet_no_mention = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775814,
    id_str="1040981111734775814",
    full_text="Thank you, that is all.",
    in_reply_to_status_id=None,
    in_reply_to_status_id_str=None,
    in_reply_to_user_id=None,
    in_reply_to_user_id_str=None,
    in_reply_to_screen_name=None,
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

thread_tweet1 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775809,
    id_str="1040981111734775809",
    full_text="TweetsToText is a bot that lives on Twitter.",
    in_reply_to_status_id=1040981111734775808,
    in_reply_to_status_id_str="1040981111734775808",
    in_reply_to_user_id=user['id'],
    in_reply_to_user_id_str=user['id_str'],
    in_reply_to_screen_name='Bot2BotAction',
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

thread_tweet2 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775810,
    id_str="1040981111734775810",
    full_text="It collects your tweets into plain text files.",
    in_reply_to_status_id=1040981111734775809,
    in_reply_to_status_id_str="1040981111734775809",
    in_reply_to_user_id=user['id'],
    in_reply_to_user_id_str=user['id_str'],
    in_reply_to_screen_name='Bot2BotAction',
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

thread_tweet3 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775811,
    id_str="1040981111734775811",
    full_text="So you can take your brilliant observations somewhere else.",
    in_reply_to_status_id=1040981111734775810,
    in_reply_to_status_id_str="1040981111734775810",
    in_reply_to_user_id=user['id'],
    in_reply_to_user_id_str=user['id_str'],
    in_reply_to_screen_name='Bot2BotAction',
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

thread_tweet4 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775812,
    id_str="1040981111734775812",
    full_text="This bot was made in the @%s." % user2['screen_name'],
    in_reply_to_status_id=1040981111734775811,
    in_reply_to_status_id_str="1040981111734775811",
    in_reply_to_user_id=user['id'],
    in_reply_to_user_id_str=user['id_str'],
    in_reply_to_screen_name='Bot2BotAction',
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            user2,
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

thread_tweet5 = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775813,
    id_str="1040981111734775813",
    full_text="You can find out more here: https://t.co/1YJGc8kavu.",
    in_reply_to_status_id=1040981111734775812,
    in_reply_to_status_id_str="1040981111734775812",
    in_reply_to_user_id=user['id'],
    in_reply_to_user_id_str=user['id_str'],
    in_reply_to_screen_name='Bot2BotAction',
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[
            dict(
                url='https://t.co/1YJGc8kavu',
                expanded_url="https://www.tweetstotext.io"
            ),
        ],
        user_mentions=[],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

thread_final_mention = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775814,
    id_str="1040981111734775814",
    full_text="Thank you, that is all. @TweetsToText",
    in_reply_to_status_id=1040981111734775813,
    in_reply_to_status_id_str="1040981111734775813",
    in_reply_to_user_id=user['id'],
    in_reply_to_user_id_str=user['id_str'],
    in_reply_to_screen_name='Bot2BotAction',
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[
            bot,
        ],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

self_reply_to_init_mention = dict(
    created_at="Sat Sep 15 15:10:12 +0000 2018",
    id=1040981111734775812,
    id_str="1040981111734775812",
    full_text="This bot was made in the RJI Futures Lab. @TweetsToText",
    in_reply_to_status_id=init_mention['id'],
    in_reply_to_status_id_str=init_mention['id_str'],
    in_reply_to_user_id=user['id'],
    in_reply_to_user_id_str=user['id_str'],
    in_reply_to_screen_name='Bot2BotAction',
    user=user,
    is_quote_status=False,
    entities=dict(
        hashtags=[],
        urls=[],
        user_mentions=[bot],
        symbols=[]
    ),
    timestamp_ms="1537024212188",
)

account_activity_w_follow_event = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[follow_event],
    unfollow_events=[],
    tweet_create_events=[],
)

account_activity_w_unfollow_event = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[],
    unfollow_events=[unfollow_event],
    tweet_create_events=[],
)

account_activity_w_bot_event = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[bot_follow_event],
    unfollow_events=[],
    tweet_create_events=[],
)

account_activity_w_mention = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[],
    unfollow_events=[],
    tweet_create_events=[init_mention],
)

account_activity_w_quoted_mention = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[],
    unfollow_events=[],
    tweet_create_events=[quoted_mention],
)

account_activity_w_reply_mention = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[],
    unfollow_events=[],
    tweet_create_events=[reply_mention],
)

account_activity_w_retweet_mention = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[],
    unfollow_events=[],
    tweet_create_events=[retweet_mention],
)

account_activity_w_final_mention = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[],
    unfollow_events=[],
    tweet_create_events=[final_mention],
)

account_activity_w_threaded_final_mention = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[],
    unfollow_events=[],
    tweet_create_events=[thread_final_mention],
)

account_activity_w_self_reply_to_init_mention = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[],
    unfollow_events=[],
    tweet_create_events=[self_reply_to_init_mention],
)

account_activity_w_request_by_dm = dict(
    for_user_id=settings.BOT_ACCOUNT_ID_STR,
    follow_events=[],
    unfollow_events=[],
    tweet_create_events=[],
    direct_message_events=[
        dict(
            type="message_create",
            created_timestamp=1561041559216,
            id=1141717166443528196,
            message_create=dict(
                message_data=dict(
                    entities=dict(
                        urls=[
                            dict(expanded_url="https://twitter.com/%s/status/%s" % (user['id'], tweet1['id']))  # noqa: E501
                        ],
                    ),
                ),
                sender_id="1141010176809398273",
                target=dict(recipient_id="1017142357932769280")
            ),
        ),
    ],
)

tweets = [tweet1, tweet2, tweet3, tweet4, tweet5, final_mention]

threaded_tweets = [
    thread_tweet1, thread_tweet2, thread_tweet3, thread_tweet4, thread_tweet5,
    thread_final_mention
]

tweets_without_mentions = [
    tweet1, tweet2, tweet3, tweet4, tweet5, final_tweet_no_mention
]

formatted_text = """Going live

TweetsToText is a bot that lives on Twitter.

It collects your tweets into plain text files.

So you can take your brilliant observations somewhere else.

This bot was made in the RJI Futures Lab.

You can find out more here: https://www.tweetstotext.io.

Thank you, that is all."""
