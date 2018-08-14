# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for handling Twitter account activity.
"""
from .follow import handle as handle_follow_event
from .mention import handle as handle_mention_event
from ..job import handle as handle_job


def is_follow(event, for_user_id):
    """
    Return True if the event signals a follow-back.
    """
    self_follow = event['source']['id'] == for_user_id
    if event['type'] == 'follow' and not self_follow:
        return True
    else:
        return False


def is_job_action(event, for_user_id):
    """
    Return True if the event signals a job action
    """
    # ASSUME: no jobs for the bot account
    authored_by_bot = event['user']['id'] == for_user_id
    # ASSUME: no jobs initiated or completed via quote tweet
    is_quote_tweet = event['is_quote_status']
    # ASSUME: no jobs initiated or completed via reply  
    is_reply = (
        bool(event['in_reply_to_user_id']) or 
        bool(event['in_reply_to_status_id'])
    )
    # ASSUME: no jobs initiated or completed via retweet
    is_retweet = 'retweeted_status' in event.keys()
    if (
        not authored_by_bot and
        not is_quote_tweet and
        not is_reply and
        not is_retweet
        
    ):
        return True
    else:
        return False


def handle(account_activity):
    """
    Handle incoming Twitter account activity.

    Return a dict with types and counts of event received and processed.    
    """
    for_user_id = account_activity['for_user_id']
    # TODO: append to this as stuff is processed
    response = []

    if 'follow_events' in account_activity.keys():
        for event in account_activity['follow_events']:
            if is_follow(event, for_user_id):
                handle_follow_event(event)
    if 'tweet_create_events' in account_activity.keys():
        for event in account_activity['tweet_create_events']:
            if is_job_action(event, for_user_id):
                created, job = handle_mention_event(event)
                if not created:
                    handle_job(job)
    # if 'tweet_delete_events' in account_activity.keys():
    # TODO: Do we receive these for tweets that mention the bot?
    # if so, maybe delete jobs associated with deleted tweets.

    # if 'direct_message_events' in account_activity.keys():
    # TODO: do something cute when the user says "hello", "thanks", "bye"

    # TODO: append stuff that was not processed

    return response
