#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Blueprint and routes for webhooks with Twitter.
"""
import base64
from datetime import datetime
import hashlib
import hmac
import json
import os
from flask import Blueprint, current_app, request
from tweets2text.handlers import handle_account_activity
from tweets2text.dynamodb import get_table


bp = Blueprint('twitter_webhook', __name__)

## TODO: add security checks
# 1. "Optional signature header validation" in https://developer.twitter.com/en/docs/accounts-and-users/subscribe-account-activity/guides/securing-webhooks
# 2. "Additional security guidelines" in same
# 3. maybe handle by decorating both of these

# Twitter makes GET method calls to this route to perform a CRC check
@bp.route('/', methods=['GET'])
def webhook_challenge():
    crc = request.args['crc_token']
  
    validation = hmac.new(
        key=bytes(current_app.config['TWITTER_CONSUMER_SECRET'], 'utf-8'),
        msg=bytes(crc, 'utf-8'),
        digestmod = hashlib.sha256
    )
    digested = base64.b64encode(validation.digest())
    response = {
        'response_token': 'sha256=' + format(str(digested)[2:-1])
    }

    return json.dumps(response)


# Twitter makes POST method calls to this route to push any account activity
@bp.route('/', methods=['POST'])
def event_listener():
    account_activity = request.get_json()
    # need to convert every empty string value in account_activity into None
    item = {
        'created_at': datetime.now().isoformat(),
        'account_activity': json.dumps(account_activity),
    }

    get_table('account-activity').put_item(Item=item)
    if os.getenv('FLASK_ENV') == 'development':
        response = handle_account_activity(account_activity)

    return json.dumps(response)
