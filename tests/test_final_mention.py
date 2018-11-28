"""Test behavior after initial mentions of the bot account."""
import json
import pytest # noqa
from tweets2text.handlers.job import get_init_tweet, get_tweet_text
from .context_setters import dynamodb_set


def test_final_mention_new_job(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        ):
    """Confirm final mention does not create new item in jobs table."""
    with dynamodb_set(app, dynamodb_w_pending_job):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )
            table_scan = dynamodb_w_pending_job.Table(
                'TweetsToText-jobs'
            ).scan(Select='COUNT')['Count']

    assert table_scan == 1


def test_final_mention_get_tweets_count(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        ):
    """Confirm only 1 API call to get tweets after final mention event."""
    with dynamodb_set(app, dynamodb_w_pending_job):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )

    assert mock_statuses_user_timeline.call_count == 1


def test_final_mention_dm_count(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        ):
    """Confirm only 1 API call to send dm after final mention event."""
    with dynamodb_set(app, dynamodb_w_pending_job):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )
    assert mock_direct_messages_new.call_count == 1


def test_tweets_stored(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        tweet_set
        ):
    """Confirm tweets are stored in jobs table."""
    with dynamodb_set(app, dynamodb_w_pending_job):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )
            job = dynamodb_w_pending_job.Table(
                'TweetsToText-jobs'
            ).scan()['Items'][0]
    assert job['tweets'] == json.dumps(tweet_set)


def test_formatted_text(init_mention, tweet_set, formatted_text):
    """Confirm text was properly formatted."""
    init_mention['full_text'] = init_mention['text']
    tweet_set.append(init_mention)
    assert get_tweet_text(tweet_set) == formatted_text


def test_final_mention_response_count(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new
        ):
    """Confirm final_mentions count of 1 after final mention event."""
    with dynamodb_set(app, dynamodb_w_pending_job):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )
    assert response.get_json()['final_mentions'] == 1



def test_self_reply_with_job(
        app, dynamodb_w_pending_job, self_reply_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        user_account, init_mention, self_reply_mention
        ):
    """Confirm self reply with pending job closes job."""
    with dynamodb_set(app, dynamodb_w_pending_job):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=self_reply_mention_activity
            )

            jobs_table = dynamodb_w_pending_job.Table(
                'TweetsToText-jobs'
            )

    job = jobs_table.get_item(
        Key=dict(
            user_id=user_account['id'],
            init_tweet_id=init_mention['id']
        )
    )['Item']

    assert job['final_tweet_id'] == self_reply_mention['id']
