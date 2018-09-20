"""
Functions for handling tweet2text jobs.
"""
import json
from uuid import uuid4
from TwitterAPI import TwitterPager
from tweets2text.dynamodb import get_table
from tweets2text.s3 import get_bucket, get_s3_file_url
from tweets2text.twitter_api import get_api, send_dm


def get_tweets(user_id, since_id, max_id):
    """
    Get tweets from user_id's timeline after since_id up to max_id.

    Return a list of dicts.
    """
    params = {
        'user_id': user_id,
        'since_id': since_id,
        'max_id': max_id,
        'count': 200,
        'include_rts': True,
    }

    response = get_api().request(
        'statuses/user_timeline',
        params,
    )

    if len(response.json()) > 199:
        pager = TwitterPager(
            get_api(), 'statuses/user_timeline', params
        )
        tweets = []
        for i in pager.get_iterator(wait=3.5):
            tweets.append(i['text'])
    else:
        tweets = response.json()

    return tweets


def store_tweets(user_id, init_tweet_id, tweets):
    """
    Add tweets attribute to DynamoDb job table item.
    """
    jobs_table = get_table('jobs')
    update = jobs_table.update_item(
        Key={
            'user_id': user_id, 
            'init_tweet_id': init_tweet_id
        },
        UpdateExpression='SET tweets = :val1',
        ExpressionAttributeValues={':val1': json.dumps(tweets)}
    )
    return update


def get_tweet_text(tweets):
    """
    Sort and format text from tweets.

    More specifically:
        1. Sort from earliest to latest tweet.
        2. Add two newlines between each tweet.
        3. TODO: Attribute re-tweets to the original author.
        4. TODO: Denote replies.
        5. Remove bot @TweetsToText from the final tweet.

    Return a string.
    """
    sorted_tweets = sorted(tweets, key=lambda k: k['id'])
    
    last_tweet = sorted_tweets.pop(-1)
    last_tweet['text'] = last_tweet['text'].replace(
        '@TweetsToText', ''
    ).strip()
    sorted_tweets.append(last_tweet)

    return '\n\n'.join([ i['text'] for i in sorted_tweets ])


def write_to_s3(tweet_text):
    """
    Write tweet_text to a .txt file in the S3 bucket.

    Generate a uuid4 that, combined with ".txt", becomes the S3 key.

    Returns the key.
    """
    bucket = get_bucket()
    file_uuid = uuid4()
    key = "%s.txt" % str(file_uuid)

    bucket.put_object(
        ACL='public-read',
        Body=tweet_text,
        Key=key,
    )

    return key


def store_s3_key(user_id, init_tweet_id, key):
    """
    Add key from S3 to related item in jobs DynamoDB table.
    """
    jobs_table = get_table('jobs')
    update = jobs_table.update_item(
        Key={
            'user_id': user_id, 
            'init_tweet_id': init_tweet_id
        },
        UpdateExpression='SET s3_key = :val1',
        ExpressionAttributeValues={':val1': key}
    )
    return update


@task(capture_response=True)
def handle(job):
    """
    Handle a job.

    More specifically:
        1. Get all the tweets
        2. Store them in DyanmoDB
        3. Sort and format the tweet text
        4. Store the tweet texts in S3
        5. Send a direct message to the user.

    Return a Twitter.
    """
    user_id = job['user_id']
    init_tweet_id = job['init_tweet_id']
    final_tweet_id = job['final_tweet_id']

    tweets = get_tweets(user_id, init_tweet_id, final_tweet_id)
    store_tweets(user_id, init_tweet_id, tweets)

    tweet_text = get_tweet_text(tweets)
    key = write_to_s3(tweet_text)
    store_s3_key(user_id, init_tweet_id, key)

    url = get_s3_file_url(key)
    # TODO: Maybe format the message to be more user-friendly
    response = send_dm(user_id, url)
    return response
