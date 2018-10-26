"""
Unit tests.
"""
from contextlib import contextmanager
import unittest
from flask import appcontext_pushed, g
import boto3
import requests_mock
from tweets2text import create_app
from tweets2text.dynamodb import get_dynamodb, schema


@contextmanager
def dynamodb_set(app, dynamodb_resource):
    def handler(sender, **kwargs):
        g.dynamodb = dynamodb_resource
    with appcontext_pushed.connected_to(handler, app):
        yield


@contextmanager
def s3_set(app, s3_resource):
    def handler(sender, **kwargs):
        g.s3 = s3_resource
    with appcontext_pushed.connected_to(handler, app):
        yield


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


outgoing_follow = {
        "for_user_id": "1017142357932769280",
        "follow_events": [
            {
                "type": "follow",
                "created_timestamp": "1535652417571",
                "target": {
                    "id": "1029178631921303553",
                    "name": "Bot2BotAction",
                },
                "source": {
                    "id": "1017142357932769280",
                    "name": "TweetToText",
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


class TestIndexView(TestTweetsToTextBase):
    """
    Test case for index view.
    """
    def test_index_view(self):
        """
        Confirm the index responds with OK status.
        """
        with self.app.test_client() as c:
            response = c.get('/')

        self.assertEqual(response.status_code, 200)


class TestDynamoDbBase(TestTweetsToTextBase):
    """
    Base class for all TweetsToText test cases involving DynamoDb
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up the test case.
        """
        super(TestDynamoDbBase, cls).setUpClass()
        
        cls.dynamodb_local = boto3.resource(
            'dynamodb', endpoint_url='http://localhost:8000'
        )
        # start the local DynamoDb instance
        # java -Djava.library.path=./DynamoDBLocal_lib -jar /tmp/dynamodb/DynamoDBLocal.jar -sharedDb
        for table_def in schema:
            try:
                cls.dynamodb_local.create_table(**table_def)
            except:
                pass

    @classmethod
    def tearDownClass(cls):
        for table_def in schema:
            table_name = table_def['TableName']
            cls.dynamodb_local.Table(table_name).delete()



class TestIncomingFollow(TestDynamoDbBase):
    """
    Test case for incoming follow account activity event.
    """
    @classmethod
    @requests_mock.Mocker()
    def setUpClass(cls, m):
        """
        Set up the test case.
        """
        super(TestIncomingFollow, cls).setUpClass()
        
        cls.m = m.register_uri(
            'POST', 
            'https://api.twitter.com/1.1/friendships/create.json',
            json=dict()
        )

        with dynamodb_set(cls.app, cls.dynamodb_local):
            with cls.app.test_client() as c:
                cls.response = c.post(
                    '/webhooks/twitter/',
                    json=incoming_follow
                )

    def test_saved(self):
        """
        Confirm that the account activity event was saved.
        """        
        table_scan = self.dynamodb_local.Table(
            'TweetsToText-account-activity'
        ).scan(Select='COUNT')

        self.assertEqual(table_scan['Count'], 1)

    def test_calls_to_twitter(self):
        """
        Confirm that Twitter was called only once.
        """
        self.assertEqual(self.m.call_count, 1)

    def test_new_followers_count(self):
        """
        Confirm the new_followers count in response is correct.
        """
        count_new_followers = self.response.json['new_followers']
        self.assertEqual(count_new_followers, 1)


class TestOutgoingFollow(TestDynamoDbBase):
    """
    Test case for outgoing follow account activity event.
    """
    @classmethod
    @requests_mock.Mocker()
    def setUpClass(cls, m):
        """
        Set up the test case.
        """
        super(TestOutgoingFollow, cls).setUpClass()
        
        cls.m = m.register_uri(
            'POST', 
            'https://api.twitter.com/1.1/friendships/create.json',
            json=dict()
        )

        with dynamodb_set(cls.app, cls.dynamodb_local):
            with cls.app.test_client() as c:
                cls.response = c.post(
                    '/webhooks/twitter/',
                    json=outgoing_follow
                )

    def test_calls_to_twitter(self):
        """
        Confirm that Twitter was called only once.
        """
        self.assertEqual(self.m.call_count, 0)

    def test_new_followers_count(self):
        """
        Confirm the new_followers count in response is correct.
        """
        count_new_followers = self.response.json['new_followers']
        self.assertEqual(count_new_followers, 0)


# class TestInitialMention
# class TestFinalMention
