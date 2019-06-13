import re
from requests_mock import Mocker
from django.test import TestCase
from tweets2text import fixtures
from tweets2text.models import TweetTextCompilation, User
from .base import (
    AccountActivityTestBase, CreateTweetBaseTest, ThreadedTweetBaseTest
)


class MentionByNonfollowerTestCase(CreateTweetBaseTest, TestCase):
    """Test case for mention by user who doesn't follow TweetsToText."""

    account_activity = fixtures.account_activity_w_mention
    friendship_lookup_response = [dict(connections=[])]

    def test_compilation_count(self):
        count = TweetTextCompilation.objects.count()
        self.assertEqual(0, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_statuses_update_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_update_endpoint.call_count,
        )

    def test_statuses_show_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_show_endpoint.call_count,
        )


class InitMentionByFollowerTestCase(CreateTweetBaseTest, TestCase):
    """Test case for an initial mention by TweetsToText follower."""

    account_activity = fixtures.account_activity_w_mention

    @classmethod
    def setUpTestData(cls):
        user_data = fixtures.user.copy()
        user_data['json_data'] = fixtures.user
        User.objects.create(**user_data)

    def test_compilation_count(self):
        count = TweetTextCompilation.objects.count()
        self.assertEqual(1, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_init_tweet_json(self):
        compilation = TweetTextCompilation.objects.all()[0]
        self.assertEqual(
            fixtures.init_mention['id_str'], compilation.init_tweet.id_str
        )

    def test_statuses_show_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_show_endpoint.call_count,
        )

    def test_statuses_update_call_count(self):
        self.assertEqual(
            1, self.mock_statuses_update_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )

    def test_dm_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )


class QuotedMentionTestCase(CreateTweetBaseTest, TestCase):
    """Test case for a quoted mention."""

    account_activity = fixtures.account_activity_w_quoted_mention

    def test_compilation_count(self):
        count = TweetTextCompilation.objects.count()
        self.assertEqual(0, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_statuses_update_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_update_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )

    def test_dm_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )


class NonAuthorReplyMentionTestCase(CreateTweetBaseTest, TestCase):
    """Test case for reply by bot follower who isn't author of init mention."""

    account_activity = fixtures.account_activity_w_reply_mention

    def test_compilation_count(self):
        count = TweetTextCompilation.objects.count()
        self.assertEqual(0, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_statuses_show_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_show_endpoint.call_count,
        )

    def test_statuses_update_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_update_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )

    def test_dm_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )


class RetweetMentionTestCase(CreateTweetBaseTest, TestCase):
    """Test case for retweet of init mention."""

    account_activity = fixtures.account_activity_w_retweet_mention

    def test_compilation_count(self):
        count = TweetTextCompilation.objects.count()
        self.assertEqual(0, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_statuses_show_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_show_endpoint.call_count,
        )

    def test_statuses_update_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_update_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )

    def test_dm_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )


class FinalMentionByFollowerTestCase(CreateTweetBaseTest, TestCase):
    """Test case for final mention by TweetsToText follower."""

    account_activity = fixtures.account_activity_w_final_mention

    @classmethod
    def setUpTestData(self):
        user_data = fixtures.user.copy()
        user_data['json_data'] = fixtures.user
        user = User.objects.create(**user_data)
        user.compilations.create(init_tweet_json=fixtures.init_mention)

    def test_compilation_count(self):
        count = TweetTextCompilation.objects.count()
        self.assertEqual(1, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_statuses_show_call_count(self):
        self.assertEqual(
            1, self.mock_statuses_show_endpoint.call_count,
        )

    def test_statuses_update_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_update_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            1, self.mock_dm_endpoint.call_count,
        )

    def test_dm_call_count(self):
        self.assertEqual(
            1, self.mock_dm_endpoint.call_count,
        )

    def test_final_tweet_json(self):
        compilation = TweetTextCompilation.objects.all()[0]
        self.assertEqual(
            fixtures.final_mention['id_str'], compilation.final_tweet.id_str
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


class DeletedInitMentionTestCase(AccountActivityTestBase, TestCase):
    """Test case for a deleted init mention."""

    account_activity = fixtures.account_activity_w_final_mention
    friendship_lookup_response = [dict(connections=['followed_by'])]

    @classmethod
    def setUpTestData(self):
        user_data = fixtures.user.copy()
        user_data['json_data'] = fixtures.user
        user = User.objects.create(**user_data)
        user.compilations.create(init_tweet_json=fixtures.init_mention)

    @Mocker()
    def setUp(self, m):

        friendship_lookup_url_pattern = re.compile(
            r'https\://api\.twitter\.com/1\.1/friendships/lookup\.json\?user_id\=\d+' # noqa
        )
        self.mock_friendship_lookup_endpoint = m.register_uri(
            'GET',
            friendship_lookup_url_pattern,
            json=self.friendship_lookup_response,
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
            json=dict(),
            status_code=404,
        )

        self.mock_statuses_update_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/statuses/update.json',
            json=dict()
        )

        self.mock_typing_indicator_endpoint = m.register_uri(
            'POST',
            'https://api.twitter.com/1.1/direct_messages/indicate_typing.json',
            json=dict()
        )

        self.mock_user_timeline_endpoint = m.register_uri(
            'GET',
            'https://api.twitter.com/1.1/statuses/user_timeline.json',
            json=fixtures.tweets
        )

        super(DeletedInitMentionTestCase, self).setUp()

    def test_deleted_compilation_count(self):
        count = TweetTextCompilation.objects.filter(
            init_tweet_deleted=True
        ).count()
        self.assertEqual(1, count)

    def test_pending_compilation_count(self):
        user = User.objects.all()[0]
        count = user.compilations.pending().count()
        self.assertEqual(1, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_statuses_show_call_count(self):
        self.assertEqual(
            1, self.mock_statuses_show_endpoint.call_count,
        )

    def test_statuses_update_call_count(self):
        self.assertEqual(
            1, self.mock_statuses_update_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )

    def test_dm_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )

    def test_init_tweet_json(self):
        compilation = TweetTextCompilation.objects.pending()[0]
        self.assertEqual(
            fixtures.final_mention['id_str'], compilation.init_tweet.id_str
        )

    def test_compilation_view_response(self):
        compilation = TweetTextCompilation.objects.all()[0]
        response = self.client.get(
            compilation.get_absolute_url()
        )
        self.assertEqual(response.status_code, 404)


class SelfReplyPendingCompilationTestCase(ThreadedTweetBaseTest, TestCase):
    """Test case for reply by init mention author w/ pending compilation."""

    account_activity = fixtures.account_activity_w_threaded_final_mention
    friendship_lookup_response = [dict(connections=['followed_by'])]

    @classmethod
    def setUpTestData(self):
        user_data = fixtures.user.copy()
        user_data['json_data'] = fixtures.user
        user = User.objects.create(**user_data)
        user.compilations.create(init_tweet_json=fixtures.init_mention)

    def test_compilation_count(self):
        count = TweetTextCompilation.objects.count()
        self.assertEqual(1, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_statuses_show_call_count(self):
        self.assertEqual(
            1, self.mock_statuses_show_endpoint.call_count,
        )

    def test_statuses_update_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_update_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            1, self.mock_dm_endpoint.call_count,
        )

    def test_dm_call_count(self):
        self.assertEqual(
            1, self.mock_dm_endpoint.call_count,
        )

    def test_final_tweet_json(self):
        compilation = TweetTextCompilation.objects.all()[0]
        self.assertEqual(
            fixtures.final_mention['id_str'], compilation.final_tweet.id_str
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


class SelfReplyNoPendingCompilationTestCase(ThreadedTweetBaseTest, TestCase):
    """Test case for reply by init mention author w/o pending compilation."""

    account_activity = fixtures.account_activity_w_threaded_final_mention

    @classmethod
    def setUpTestData(self):
        user_data = fixtures.user.copy()
        user_data['json_data'] = fixtures.user
        User.objects.create(**user_data)

    def test_compilation_count(self):
        count = TweetTextCompilation.objects.count()
        self.assertEqual(0, count)

    def test_friendship_lookup_call_count(self):
        self.assertEqual(
            1, self.mock_friendship_lookup_endpoint.call_count
        )

    def test_statuses_update_call_count(self):
        self.assertEqual(
            0, self.mock_statuses_update_endpoint.call_count,
        )

    def test_typing_indicator_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )

    def test_dm_call_count(self):
        self.assertEqual(
            0, self.mock_dm_endpoint.call_count,
        )
