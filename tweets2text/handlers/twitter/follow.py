# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for handling Twitter follow events.
"""
from tweets2text.twitter_api import get_api


@task(capture_response=True)
def handle(event):
    """
    Follow the source of a follow event.

    Return a TwitterResponse instance.
    """
    user_to_follow = event['source']['id']
    response = get_api().request(
        'friendships/create', {'user_id': user_to_follow}
    )
    response.response.raise_for_status()
    return response
