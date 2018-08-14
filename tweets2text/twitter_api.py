# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import current_app, g
from TwitterAPI import TwitterAPI


def get_api():
    if 'twitter_api' not in g:
        g.twitter_api = TwitterAPI(
            current_app.config['TWITTER_CONSUMER_KEY'],
            current_app.config['TWITTER_CONSUMER_SECRET'],
            current_app.config['TWITTER_ACCESS_TOKEN'],
            current_app.config['TWITTER_ACCESS_TOKEN_SECRET'],
        )

    return g.twitter_api


def send_dm(to_user_id, message_text):
    """
    Send direct message to user_id with URL to key.
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
