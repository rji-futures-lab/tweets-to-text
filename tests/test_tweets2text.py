"""
Unit tests.
"""
import unittest
from flask import current_app, g
from moto import mock_dynamodb
import requests_mock
from tweets2text import create_app
from tweets2text.dynamodb import get_dynamodb
# from tweets2text.handlers.twitter import handle_account_activity


incoming_follow = {
    "for_user_id": "1017142357932769280",
    "follow_events": [
        {
            "type": "follow",
            "created_timestamp": "1535652417571",
            "target": {
                "id": "1017142357932769280",
                "name": "TweetToText",
            },
            "source": {
                "id": "1029178631921303553",
                "name": "Bot2BotAction",  
            }
        }
    ]
}


class TestTweetsToTextBase(unittest.TestCase):
    """
    Base class for all TweetsToText test cases.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the test case.
        """
        cls.app = create_app({
            'TESTING': True,
        })

        cls.client = cls.app.test_client()


class TestIndexView(TestTweetsToTextBase):
    """
    Test case for index view.
    """
    def test_index_view(self):
        """
        Confirm the index responds with OK status.
        """
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)


class TestIncomingFollow(TestTweetsToTextBase):
    """
    Test case for incoming follow account activity event.
    """
    @classmethod
    @mock_dynamodb
    @requests_mock.Mocker()
    def setUpClass(cls, m):
        """
        Set up the test case.
        """
        super(TestIncomingFollow, cls).setUpClass()

        m.register_uri(
            'POST', 
            'https://api.twitter.com/1.1/friendships/create.json',
            json=dict()
        )

        with cls.app.app_context():
            cls.dynamodb = get_dynamodb()
            cls.app.logger.info('inside with app_context()')
            cls.app.logger.info('cls.dynamodb')
            cls.app.logger.info(id(cls.dynamodb))
            cls.app.logger.info('g.dynamodb')
            cls.app.logger.info(id(g.dynamodb))

            cls.response = cls.client.post(
                '/webhooks/twitter/',
                json=incoming_follow
            )

    def test_saved(self):
        """
        Confirm that the account activity event was saved.
        """
        self.app.logger.info('inside test_saved()')
        self.app.logger.info('self.dynamodb')
        self.app.logger.info(id(self.dynamodb))

        table = self.dynamodb.Table(
            'TweetsToText-account-activity'
        )

        scan = table.scan(Select='COUNT')

        self.assertEqual(scan['Count'], 1)

# class TestOutgoingFollow
# class TestInitialMention
# class TestFinalMention
