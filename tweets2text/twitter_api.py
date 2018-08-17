# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from dotenv import load_dotenv
from TwitterAPI import TwitterAPI


def get_api():
    """
    Get an authenticated connection to Twitter's API.

    Return a `TwitterAPI` instance.
    """
    env_loaded = bool(
        os.getenv('TWITTER_CONSUMER_KEY') and 
        os.getenv('TWITTER_CONSUMER_SECRET') and
        os.getenv('TWITTER_ACCESS_TOKEN') and
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

    if not env_loaded:
        print(' Environment variables are missing. Loading...')
        load_dotenv()
        print(
                os.getenv('TWITTER_CONSUMER_KEY'),
                os.getenv('TWITTER_CONSUMER_SECRET'),
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )

    twitter_api = TwitterAPI(
        os.getenv('TWITTER_CONSUMER_KEY'),
        os.getenv('TWITTER_CONSUMER_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

    return twitter_api


def get_api_env():
    """
    Return the Twitter API environment (configured in .env file).
    """
    if not os.getenv('TWITTER_API_ENV'):
        load_dotenv()

    return os.getenv('TWITTER_API_ENV')


def send_dm(to_user_id, message_text):
    """
    Send a direct message to user_id containing message_text.
    """
    event = {
        "event": {
            "type": "message_create",
            "message_create": {
                "target": {
                    "recipient_id": int(to_user_id),
                },
                "message_data": {
                    "text": message_text,
                }
            }
        }
    }

    response = get_api().request(
        'direct_messages/events/new',
        json.dumps(event),
    ).response

    response.raise_for_status()
    
    return response
