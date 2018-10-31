"""Test behavior after initial mentions of the bot account."""
import json
import pytest # noqa
from .context_setters import aws_resources_set


def test_final_mention_new_job(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        s3_bucket
        ):
    """Confirm final mention does not create new item in jobs table."""
    with aws_resources_set(app, dynamodb_w_pending_job, s3_bucket):
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
        s3_bucket
        ):
    """Confirm only 1 API call to get tweets after final mention event."""
    with aws_resources_set(app, dynamodb_w_pending_job, s3_bucket):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )

    assert mock_statuses_user_timeline.call_count == 1


def test_final_mention_dm_count(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        s3_bucket
        ):
    """Confirm only 1 API call to send dm after final mention event."""
    with aws_resources_set(app, dynamodb_w_pending_job, s3_bucket):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )
    assert mock_direct_messages_new.call_count == 1


def test_tweets_stored(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        tweet_set, s3_bucket
        ):
    """Confirm tweets are stored in jobs table."""
    with aws_resources_set(app, dynamodb_w_pending_job, s3_bucket):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )
            job = dynamodb_w_pending_job.Table(
                'TweetsToText-jobs'
            ).scan()['Items'][0]
    assert job['tweets'] == json.dumps(tweet_set)


def test_write_to_s3(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        s3_bucket, formatted_text
        ):
    """Confirm text was properly written to S3 bucket."""
    with aws_resources_set(app, dynamodb_w_pending_job, s3_bucket):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )
            key = [i.key for i in s3_bucket.objects.all()][0]
            local_file_path = '/tmp/%s' % key
            s3_bucket.download_file(key, local_file_path)

            with open(local_file_path) as f:
                saved_text = f.read()
    assert saved_text == formatted_text


def test_final_mention_response_count(
        app, dynamodb_w_pending_job, final_mention_activity,
        mock_statuses_user_timeline, mock_direct_messages_new,
        s3_bucket
        ):
    """Confirm final_mentions count of 1 after final mention event."""
    with aws_resources_set(app, dynamodb_w_pending_job, s3_bucket):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=final_mention_activity
            )
    assert response.get_json()['final_mentions'] == 1
