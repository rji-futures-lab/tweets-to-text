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
