import re
from requests_mock import Mocker
from django.test import TestCase
from tweets2text import fixtures
from tweets2text.models import TweetTextCompilation, User
from .base import (
    AccountActivityTestBase, CreateTweetBaseTest, ThreadedTweetBaseTest
)


class CompilationByDMTestCase(AccountActivityTestBase, TestCase):
    """Test case for receiving a compilation request via DM."""

    account_activity = fixtures.account_activity_w_request_by_dm

    @Mocker()
    def setUp(self, m):

        friendship_lookup_url_pattern = re.compile(
            r'https\://api\.twitter\.com/1\.1/friendships/lookup\.json\?user_id\=\d+' # noqa
        )
        self.mock_friendship_lookup_endpoint = m.register_uri(
            'GET',
            friendship_lookup_url_pattern,
            json=[dict(connections=['followed_by'])]
        )

        self.mock_dm_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/direct_messages/events/new.json',
            json=dict()
        )

        statuses_show_url_pattern = re.compile(
            r'https\://api\.twitter\.com/1\.1/statuses/show\/\d+\.json'
        )
        self.mock_statuses_show_endpoint = m.register_uri(
            'GET',
            statuses_show_url_pattern,
            json=fixtures.init_tweet_no_mention_full_text,
        )

        self.mock_typing_indicator_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/direct_messages/indicate_typing.json',
            json=dict()
        )

        self.mock_user_timeline_endpoint = m.register_uri(
            'GET',
            'https://api.twitter.com/1.1/statuses/user_timeline.json',
            json=fixtures.tweets_without_mentions
        )

        super(CompilationByDMTestCase, self).setUp()

    @classmethod
    def setUpTestData(cls):
        user_data = fixtures.user.copy()
        user_data['json_data'] = fixtures.user
        User.objects.create(**user_data)

    def test_pending_compilation_count(self):
        count = TweetTextCompilation.objects.pending().count()
        self.assertEqual(0, count)

    def test_completed_compilation_count(self):
        count = TweetTextCompilation.objects.completed().count()
        self.assertEqual(1, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_statuses_show_call_count(self):
        self.assertEqual(
            1, self.mock_statuses_show_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            1, self.mock_dm_endpoint.call_count,
        )

    def test_user_timeline_call_count(self):
        self.assertEqual(
            1, self.mock_user_timeline_endpoint.call_count,
        )

    def test_dm_call_count(self):
        self.assertEqual(
            1, self.mock_dm_endpoint.call_count,
        )

    def test_tweets(self):
        compilation = TweetTextCompilation.objects.all()[0]
        self.assertTrue(
            len(compilation.tweets) > 0
        )

    def test_text(self):
        compilation = TweetTextCompilation.objects.all()[0]
        self.assertEqual(
            fixtures.formatted_text, compilation.text
        )

    def test_completed_at(self):
        compilation = TweetTextCompilation.objects.all()[0]
        self.assertTrue(compilation.completed_at)

    def test_compilation_view_response(self):
        compilation = TweetTextCompilation.objects.all()[0]
        response = self.client.get(
            compilation.get_absolute_url()
        )
        self.assertEqual(response.status_code, 200)
