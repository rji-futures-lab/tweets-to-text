"""Test behavior after initial mentions of the bot account."""
import pytest # noqa
from .context_setters import dynamodb_set


def test_init_mention_new_job(
        app, dynamodb, init_mention_activity, mock_statuses_update
        ):
    """Confirm initial mention creates new item in jobs table."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=init_mention_activity
            )
            table_scan = dynamodb.Table(
                'TweetsToText-jobs'
            ).scan(Select='COUNT')['Count']

    assert table_scan == 1


def test_init_mention_reply_count(
        app, dynamodb, init_mention_activity, mock_statuses_update
        ):
    """Confirm only 1 Twitter API after initial mention event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=init_mention_activity
            )

    assert mock_statuses_update.call_count == 1


def test_init_mention_response_count(
        app, dynamodb, init_mention_activity, mock_statuses_update
        ):
    """Confirm init_mentions count of 1 after initial mention event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=init_mention_activity
            )

    assert response.get_json()['init_mentions'] == 1

# TODO:
# test_self_mention_no_job
# test_quote_tweet_no_job
# test_reply_mention_no_job
# test_retweet_mention_no_job
# test_self_mention_response_count
# test_quote_tweet_response_count
# test_reply_mention_response_count
# test_retweet_mention_response_count
