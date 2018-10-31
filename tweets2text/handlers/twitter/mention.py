# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Functions for handling Twitter mention events."""
import json
from boto3.dynamodb.conditions import Key, Attr
from zappa.async import task
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


@task(capture_response=True)
def handle(event):
    """
    Handle an incoming mention event.

    Parse event, get pending job and update OR (if no pending job) create it.

    Return a tuple with created (boolean) and dict of job.
    """
    job = get_pending_job(event['user']['id'])

    if not job:
        job = create_job(event)
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
                ':val1': event['id'],
                ':val2': json.dumps(event),
            },
        )
        job['final_tweet_id'] = event['id']

    return created, job
