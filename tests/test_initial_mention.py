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


def test_self_mention_no_job(
        app, dynamodb, self_mention_activity, mock_statuses_update
        ):
    """Confirm self mention creates no item in jobs table."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=self_mention_activity
            )
            table_scan = dynamodb.Table(
                'TweetsToText-jobs'
            ).scan(Select='COUNT')['Count']

    assert table_scan == 0


def test_self_mention_no_reply(
        app, dynamodb, self_mention_activity, mock_statuses_update
        ):
    """Confirm no Twitter API after self mention event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=self_mention_activity
            )

    assert mock_statuses_update.call_count == 0


def test_self_mention_response_count(
        app, dynamodb, self_mention_activity, mock_statuses_update
        ):
    """Confirm init_mention count of 0 after self mention event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=self_mention_activity
            )

    assert response.get_json()['init_mentions'] == 0


def test_quote_tweet_no_job(
        app, dynamodb, quote_tweet_activity, mock_statuses_update
        ):
    """Confirm quote tweet creates no item in jobs table."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=quote_tweet_activity
            )
            table_scan = dynamodb.Table(
                'TweetsToText-jobs'
            ).scan(Select='COUNT')['Count']

    assert table_scan == 0


def test_quote_tweet_no_reply(
        app, dynamodb, quote_tweet_activity, mock_statuses_update
        ):
    """Confirm no Twitter API after quote tweet event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=quote_tweet_activity
            )

    assert mock_statuses_update.call_count == 0


def test_quote_tweet_response_count(
        app, dynamodb, quote_tweet_activity, mock_statuses_update
        ):
    """Confirm init_mention count of 0 after quote tweet event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=quote_tweet_activity
            )

    assert response.get_json()['init_mentions'] == 0


def test_reply_mention_no_job(
        app, dynamodb, reply_mention_activity, mock_statuses_update
        ):
    """Confirm reply mention creates no item in jobs table."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=reply_mention_activity
            )
            table_scan = dynamodb.Table(
                'TweetsToText-jobs'
            ).scan(Select='COUNT')['Count']

    assert table_scan == 0


def test_reply_mention_no_reply(
        app, dynamodb, reply_mention_activity, mock_statuses_update
        ):
    """Confirm no Twitter API after reply mention event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=reply_mention_activity
            )

    assert mock_statuses_update.call_count == 0


def test_reply_mention_response_count(
        app, dynamodb, reply_mention_activity, mock_statuses_update
        ):
    """Confirm init_mention count of 0 after reply mention event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=reply_mention_activity
            )

    assert response.get_json()['init_mentions'] == 0


def test_retweet_no_job(
        app, dynamodb, retweet_activity, mock_statuses_update
        ):
    """Confirm retweet mention creates no item in jobs table."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=retweet_activity
            )
            table_scan = dynamodb.Table(
                'TweetsToText-jobs'
            ).scan(Select='COUNT')['Count']

    assert table_scan == 0


def test_retweet_no_reply(
        app, dynamodb, retweet_activity, mock_statuses_update
        ):
    """Confirm no Twitter API after retweet event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            c.post(
                '/webhooks/twitter/',
                json=retweet_activity
            )

    assert mock_statuses_update.call_count == 0


def test_retweet_response_count(
        app, dynamodb, retweet_activity, mock_statuses_update
        ):
    """Confirm init_mention count of 0 after retweet event."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=retweet_activity
            )

    assert response.get_json()['init_mentions'] == 0
