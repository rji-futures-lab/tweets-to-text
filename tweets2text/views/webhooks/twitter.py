#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Blueprint for integrating with Twitter's Account Activity API."""
import os
import base64
from datetime import datetime
import hashlib
import hmac
import json
from flask import (
    Blueprint,
    current_app,
    g,
    jsonify,
    request
)
from tweets2text.dynamodb import get_dynamodb
from tweets2text.handlers import handle_account_activity
from tweets2text.s3 import get_bucket
from tweets2text.twitter_api import get_api

bp = Blueprint('twitter_webhook', __name__)


@bp.before_app_request
def load_external_resources():
    """
    Load external resources to the global app context before each request.

    Adds:
        - dynamoDb
        - s3 bucket
        - TwitterAPI
    """
    get_dynamodb()
    get_bucket()
    get_api()

# TODO: add security checks
# 1. "Optional signature header validation" in https://developer.twitter.com/en/docs/accounts-and-users/subscribe-account-activity/guides/securing-webhooks # noqa
# 2. "Additional security guidelines" in same
# 3. maybe handle by decorating both of these


@bp.route('/', methods=['GET'])
def webhook_challenge():
    """
    Perform a Challenge-Response Check (CRC) to secure the Twitter webhook.

    The CRC verifies our ownership of the app and the webhook URL with Twitter.

    Twitter makes GET method calls to this route with a crc_token, which is
    used along with TWITTER_CONSUMER_SECRET to build a response_token.

    Return JSON that includes the response_token.
    """
    crc = request.args['crc_token']

    validation = hmac.new(
        key=bytes(os.getenv('TWITTER_CONSUMER_SECRET'), 'utf-8'),
        msg=bytes(crc, 'utf-8'),
        digestmod=hashlib.sha256
    )
    digested = base64.b64encode(validation.digest())
    resp_data = {
        'response_token': 'sha256=' + format(str(digested)[2:-1])
    }
    response = jsonify(resp_data)

    return response


@bp.route('/', methods=['POST'])
def event_listener():
    """
    Route called by Twitter to announce account activity.

    Twitter makes POST method calls to this route.
    """
    account_activity = request.get_json()

    item = {
        'created_at': datetime.now().isoformat(),
        'account_activity': json.dumps(account_activity),
    }
    g.dynamodb.Table('TweetsToText-account-activity').put_item(Item=item)

    current_app.logger.info('Handling account activity event...')
    resp_data = handle_account_activity(account_activity)
    current_app.logger.info('Account activity event handled!')

    response = jsonify(resp_data)

    return response
