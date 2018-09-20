# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions for handling Twitter mention events.
"""
import json
import random
from boto3.dynamodb.conditions import Key, Attr
from zappa.async import task
from tweets2text.twitter_api import get_api
from tweets2text.dynamodb import get_table


def get_pending_job(user_id):
    """
    Get the most recent pending job for user_id.

    Return dict of item, or None.
    """
    jobs_table = get_table('jobs')
    response = jobs_table.query(
        KeyConditionExpression=Key('user_id').eq(user_id),
        # filter to items without a final_tweet_id
        FilterExpression=Attr('final_tweet_id').not_exists(),
        # with highest init_tweet_id for user_id
        ScanIndexForward=False,
    )
    try:
        job = response['Items'][0]
    except IndexError:
        job = None
    return job


def create_job(data):
    """
    Parse data and put into into table.

    Return a dict of created job.
    """
    job = {
        'user_id': data['user']['id'],
        'init_tweet_id': data['id'],
        'screen_name': data['user']['screen_name'],
        'init_event_json': json.dumps(data),
    }
    jobs_table = get_table('jobs')
    jobs_table.put_item(Item=job)

    return job


def create_or_update_job(data):
    """
    Parse data, get pending job and update OR (if no pending job) create it.

    Return tuple with created (boolean value) and dict of job.
    """
    job = get_pending_job(data['user']['id'])

    if not job:
        job = create_job(data)
        created = True
    else:
        created = False

        # update the job
        jobs_table = get_table('jobs')
        exp = 'SET final_tweet_id = :val1, final_event_json = :val2'
        jobs_table.update_item(
            Key={
                'user_id': job['user_id'],
                'init_tweet_id': job['init_tweet_id'],
            },
            UpdateExpression=exp,
            ExpressionAttributeValues={
                ':val1': data['id'],
                ':val2': json.dumps(data),
            },
        )
        job['final_tweet_id'] = data['id']

    return (created, job)


@task(capture_response=True)
def reply_to_init_mention(init_tweet_id, screen_name):
    """
    Tweet a reply to the initial the user's initial @mention of the bot.

    Return `TwitterResponse` instance.
    """
    replies = [
        'We got you', 'On it', 'Got it', 'Gotcha', 'Here for you', 'With you',
        "Let's do this", 'We on it', 'Got your back',
        '👍🏻', '👍🏼', '👍🏽', '👍🏾', '👍🏿',
        '👌🏻', '👌🏼', '👌🏽', '👌🏾', '👌🏿',
    ]

    status = '@{0} {1}'.format(screen_name, random.choice(replies))
    params = dict(status=status, in_reply_to_status_id=init_tweet_id)

    response = get_api().request('statuses/update', params)
    response.response.raise_for_status()

    return response


def handle(event):
    """
    Handle an incoming mention event.

    Creates or updates an item in the DynamoDB jobs table.

    If a new job is create, reply to the initial tweet.
    """
    created, job = create_or_update_job(event)

    if created:
        reply_to_init_mention(
            job['init_tweet_id'],
            job['screen_name'],
        )

    return created, job
