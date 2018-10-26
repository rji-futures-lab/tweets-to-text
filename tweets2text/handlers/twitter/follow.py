# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions for handling Twitter follow events."""
from time import sleep
from flask import current_app
from requests.exceptions import HTTPError
from zappa.async import task
from tweets2text import create_app
from tweets2text.twitter_api import get_api


@task(capture_response=True)
def handle(event):
    """
    Follow the source of a follow event.

    Return response from Twitter as json.
    """
    app = current_app or create_app()

    if not app.testing:
        sleep(10)

    user_to_follow = event['source']['id']
    app.logger.info('...following user_id %s' % user_to_follow)
    follow = get_api().request(
        'friendships/create', {'user_id': user_to_follow}
    )

    try:
        follow.response.raise_for_status()
    except HTTPError as e:
        msg = '{0}\n{1}'.format(
            e,
            '\n'.join([
                '{code}: {message}'.format(**i)
                for i in follow.json()['errors']
            ])
        )
        app.logger.error(msg)

    return follow.json()
