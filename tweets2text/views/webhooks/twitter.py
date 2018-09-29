#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Blueprint and routes for webhooks with Twitter.
"""
import os
import base64
from datetime import datetime
import hashlib
import hmac
import json
from flask import current_app, Blueprint, jsonify, request
from tweets2text.handlers import handle_account_activity
from tweets2text.dynamodb import get_table


bp = Blueprint('twitter_webhook', __name__)

# TODO: add security checks
# 1. "Optional signature header validation" in https://developer.twitter.com/en/docs/accounts-and-users/subscribe-account-activity/guides/securing-webhooks # noqa
# 2. "Additional security guidelines" in same
# 3. maybe handle by decorating both of these


# Twitter makes GET method calls to this route to perform a CRC check
@bp.route('/', methods=['GET'])
def webhook_challenge():
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


# Twitter makes POST method calls to this route to push any account activity
@bp.route('/', methods=['POST'])
def event_listener():
    account_activity = request.get_json()

    item = {
        'created_at': datetime.now().isoformat(),
        'account_activity': json.dumps(account_activity),
    }

    get_table('account-activity').put_item(Item=item)

    current_app.logger.info('Handling account activity event...')
    resp_data = handle_account_activity(account_activity)
    current_app.logger.info('Account activity event handled!')

    response = jsonify(resp_data)

    return response
