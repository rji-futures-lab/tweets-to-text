# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Initialize a connection to Twitter."""
import json
import os
from flask import current_app, g
from TwitterAPI import TwitterAPI
from tweets2text import create_app


def get_api():
    """
    Get an authenticated connection to Twitter's API.

    Add to application content, g.twitter_api, if missing.

    Return a `TwitterAPI` instance.
    """
    if 'twitter_api' not in g:
        g.twitter_api = TwitterAPI(
            os.getenv('TWITTER_CONSUMER_KEY'),
            os.getenv('TWITTER_CONSUMER_SECRET'),
            os.getenv('TWITTER_ACCESS_TOKEN'),
            os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        )

    return g.twitter_api


def send_dm(to_user_id, message_text):
    """Send a direct message to user_id containing message_text."""
    app = current_app or create_app()

    data = {
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

    with app.app_context():
        sent_dm = get_api().request(
            'direct_messages/events/new',
            json.dumps(data),
        )

    return sent_dm
