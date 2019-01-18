# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions for handling Twitter follow events."""
from time import sleep
from flask import current_app
from requests.exceptions import HTTPError
from zappa.async import task
from tweets2text import create_app
from tweets2text.twitter_api import send_dm, send_typing_indicator


instructions = [
    "Thanks for the follow! I'm here whenever you need me. Here's how it "
    "works:",
    "Whenever you start a new thread, be sure to mention @TweetsToText. "
    "I'll reply so you know that I've got you covered.",
    "Then tweet all your tweets, like you normally would.",
    "In your final tweet, mention @TweetsToText again.",
    "Then check back here, and I'll DM you a link to a text file with all "
    "your tweets in chronological order.",
    "You can also find out more at https://www.tweetstotext.io",
]


@task(capture_response=True)
def handle(new_follower_id):
    """
    Send entire on-boarding instructions to a new follower.

    Return response from Twitter as json.
    """
    app = current_app or create_app()

    app.logger.info('...on-boarding user_id %s' % new_follower_id)

    with app.app_context():
        for i in instructions:
            # send typing indicator
            sent_indicator = send_typing_indicator(new_follower_id)
            try:
                sent_indicator.response.raise_for_status()
            except HTTPError as e:
                msg = '{0}\n{1}'.format(
                    e,
                    '\n'.join([
                        '{code}: {message}'.format(**i)
                        for i in sent_indicator.json()['errors']
                    ])
                )
                app.logger.error(msg)

            if not app.testing:
                sleep(3.1)

            # send direct message
            sent_dm = send_dm(new_follower_id, i)
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
