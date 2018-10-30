"""Test behavior after initial mentions of the bot account."""
import pytest # noqa
from .context_setters import dynamodb_set


def test_init_mention_new_job(
        app, dynamodb, init_mention_activity, mock_statuses_update
        ):
    """Confirm that an initial mention creates a new job."""
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
    """Confirm that an initial mention creates a new job."""
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
    """Confirm that an initial mention creates a new job."""
    with dynamodb_set(app, dynamodb):
        with app.test_client() as c:
            response = c.post(
                '/webhooks/twitter/',
                json=init_mention_activity
            )

    assert response.get_json()['init_mentions'] == 1
