# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for handling Twitter follow events.
"""
from tweets2text.twitter_api import get_api


def handle(event):
    """
    Follow the source of a follow event.

    Return a TwitterResponse instance.
    """
    user_to_follow = event['source']['id']
    response = get_api().request(
        'friendships/create', {'user_id': user_to_follow}
    )

    return response
