# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions for handling Twitter follow events."""
from time import sleep
from flask import current_app
from requests.exceptions import HTTPError
from zappa.async import task
from tweets2text import create_app
from tweets2text.twitter_api import send_dm


onboard_msg = "Thanks for the follow! I'm here to help whenever you need it. "\
              "Find out more at http://tweetstotext.io."


@task(capture_response=True)
def handle(new_follower_id):
    """
    Send an on-boarding message to a new follower.

    Return response from Twitter as json.
    """
    app = current_app or create_app()

    if not app.testing:
        sleep(10)

    app.logger.info('...on-boarding user_id %s' % new_follower_id)
    sent_dm = send_dm(new_follower_id, onboard_msg)

    try:
        sent_dm.response.raise_for_status()
    except HTTPError as e:
        msg = '{0}\n{1}'.format(
            e,
            '\n'.join([
                '{code}: {message}'.format(**i)
                for i in sent_dm.json()['errors']
            ])
        )
        app.logger.error(msg)

    return sent_dm.json()
