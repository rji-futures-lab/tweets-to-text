# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from TwitterAPI import TwitterAPI


def get_api():
    """
    Get an authenticated connection to Twitter's API.

    Return a `TwitterAPI` instance.
    """
    twitter_api = TwitterAPI(
        os.getenv('TWITTER_CONSUMER_KEY'),
        os.getenv('TWITTER_CONSUMER_SECRET'),
        os.getenv('TWITTER_ACCESS_TOKEN'),
        os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    )

    return twitter_api


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
