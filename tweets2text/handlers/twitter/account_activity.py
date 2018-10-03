# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for handling Twitter account activity.
"""
from time import sleep
from flask import current_app, g
from requests.exceptions import HTTPError
from zappa.async import task
from tweets2text import create_app
from .follow import handle as handle_follow_event
from .mention import handle as handle_mention_event
from ..job import handle as handle_job


def is_follow(event, for_user_id):
    """
    Return True if the event signals a follow-back.
    """
    self_follow = int(event['source']['id']) == for_user_id
    if event['type'] == 'follow' and not self_follow:
        return True
    else:
        return False


def is_actionable_mention(event, for_user_id):
    """
    Return True if the event includes an actionable mention
    """
    authored_by_bot = event['user']['id'] == for_user_id
    is_quote_tweet = event['is_quote_status']
    is_reply = (
        bool(event['in_reply_to_status_id_str']) or
        bool(event['in_reply_to_status_id'])
    )
    is_retweet = 'retweeted_status' in event.keys()

    if (
        not authored_by_bot and
        not is_quote_tweet and
        not is_reply and
        not is_retweet

    ):
        is_actionable = True
    else:
        is_actionable = False

    return is_actionable


@task(capture_response=True)
def reply_to_init_mention(init_tweet_id, screen_name):
    """
    Tweet a reply to the user's initial @mention of the bot.

    Return `TwitterResponse` instance.
    """
    # app = create_app()
    sleep(5)

    replies = [
        'We got you', 'On it', 'Got it', 'Gotcha', 'Here for you', 'With you',
        "Let's do this", 'We on it', 'Got your back',
        '👍🏻', '👍🏼', '👍🏽', '👍🏾', '👍🏿',
        '👌🏻', '👌🏼', '👌🏽', '👌🏾', '👌🏿',
    ]

    status = '@{0} {1}'.format(screen_name, random.choice(replies))
    params = dict(status=status, in_reply_to_status_id=init_tweet_id)

    reply = get_api().request('statuses/update', params)

    try:
        reply.response.raise_for_status()
    except HTTPError as e:
        msg = '{0}\n{1}'.format(
            e,
            '\n'.join([
                '{code}: {message}'.format(**i) 
                for i in reply.json()['errors']
            ])
        )
        app.logger.error(msg)

    return response


def handle(account_activity):
    """
    Handle incoming Twitter account activity.

    Return a dict with types and counts of event received and processed.
    """
    for_user_id = int(account_activity['for_user_id'])
    response = dict(
        new_followers=0, init_mentions=0, final_mentions=0
    )

    if 'follow_events' in account_activity.keys():
        current_app.logger.info('Handling follow events...')
        for event in account_activity['follow_events']:
            if is_follow(event, for_user_id):
                current_app.logger.info('...defer on-boarding DM...')
                handle_follow_event(event)
                response['new_followers'] += 1
            else:
                current_app.logger.info('...skipping...')
        current_app.logger.info('All follow events handled!')

    if 'tweet_create_events' in account_activity.keys():
        current_app.logger.info('Handling mention events...')
        for event in account_activity['tweet_create_events']:
            if is_actionable_mention(event, for_user_id):
                created, job = handle_mention_event(event)
                if created:
                    current_app.logger.info(
                        '...defer reply to initial mention...'
                    )
                    reply_to_init_mention()
                    response['init_mentions'] += 1
                else:
                    current_app.logger.info('...defer completing job...')
                    handle_job(job)
                    response['final_mentions'] += 1
            else:
                current_app.logger.info('...skipping...')
        current_app.logger.info('All mention events handled!')

    # if 'tweet_delete_events' in account_activity.keys():
    # TODO: Do we receive these for tweets that mention the bot?
    # if so, maybe delete jobs associated with deleted tweets.

    # if 'direct_message_events' in account_activity.keys():
    # TODO: do something cute when the user says "hello", "thanks", "bye"

    # TODO: append stuff that was not processed

    return response
