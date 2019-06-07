import json
import random
import uuid
from time import sleep
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.utils import timezone
from requests.exceptions import HTTPError
from TwitterAPI import TwitterPager
import constants
from tweets2text.twitter_api import (
    Tweet, TwitterMixin, TwitterObject
)


class User(TwitterMixin, models.Model):
    id = models.BigIntegerField(
        primary_key=True,
    )
    id_str = models.CharField(
        max_length=200,
    )
    name = models.CharField(
        max_length=200,
    )
    screen_name = models.CharField(
        max_length=20,
    )
    location = models.CharField(
        max_length=200,
        blank=True,
    )
    json_data = JSONField()
    last_follow_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def has_pending_compilation(self):
        return self.compilations.pending.exists()

    @property
    def pending_compilation(self):
        return self.compilations.pending.latest('requested_at')

    def send_dm(self, message_text):
        """Send a direct message to follower containing message_text."""
        data = dict(
            event=dict(
                type="message_create",
                message_create=dict(
                    target=dict(recipient_id=self.id_str),
                    message_data=dict(text=message_text),
                )
            )
        )
        self.send_typing_indicator()
        if not settings.TESTING:
            sleep(3.1)

        sent_dm = self.twitter_api.request(
            'direct_messages/events/new',
            json.dumps(data),
        )

        return sent_dm

    def send_welcome_dm(self):
        for m in constants.instructions:
            self.send_dm(m)

    def send_typing_indicator(self):
        params = dict(recipient_id=self.id_str)

        sent_indicator = self.twitter_api.request(
            'direct_messages/indicate_typing',
            params,
        )

        return sent_indicator

    class Meta:
        indexes = [
            models.Index(
                fields=['id_str', ],
                name='id_str_index',
            ),
            models.Index(
                fields=['last_follow_at', ],
                name='last_follow_at_index',
            ),
        ]


class FollowHistory(models.Model):
    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name='follow_history',
    )
    event_json = JSONField()

    @property
    def type(self):
        return self.event_json['type']

    @property
    def created_timestamp(self):
        return self.event_json['created_timestamp']


class AccountActivity(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    received_at = models.DateTimeField(
        auto_now_add=True,
    )
    processing_started_at = models.DateTimeField(null=True)
    processing_completed_at = models.DateTimeField(null=True)
    json_data = JSONField()

    def get_events_by_type(self, message_type):
        try:
            event_list = [
                TwitterObject(**e) for e in self.json_data[message_type]
            ]
        except KeyError:
            event_list = []

        return event_list

    @property
    def direct_message_events(self):
        try:
            self._direct_message_events
        except AttributeError:
            self._direct_message_events = self.get_events_by_type(
                'direct_message_events'
            )

        return self._direct_message_events

    @property
    def follow_events(self):
        try:
            self._follow_events
        except AttributeError:
            self._follow_events = [
                f for f in self.get_events_by_type('follow_events')
                if f.type == 'follow' and
                f.target['id_str'] == self.json_data['for_user_id'] and
                f.source['id_str'] != self.json_data['for_user_id']
            ]

        return self._follow_events

    @property
    def unfollow_events(self):
        try:
            self._unfollow_events
        except AttributeError:
            self._unfollow_events = [
                f for f in self.get_events_by_type('unfollow_events')
                if f.type == 'unfollow' and
                f.target['id_str'] == self.json_data['for_user_id'] and
                f.source['id_str'] != self.json_data['for_user_id']
            ]

        return self._unfollow_events

    @property
    def tweet_create_events(self):
        try:
            self._tweet_create_events
        except AttributeError:
            self._tweet_create_events = self.get_events_by_type(
                'tweet_create_events'
            )

        return self._tweet_create_events

    class Meta:
        verbose_name = 'Account Activity'
        indexes = [
            models.Index(
                fields=['received_at', ],
                name='received_at_index',
            ),
        ]


class TweetTextCompilationManager(models.Manager):

    def pending(self):
        qs = self.get_queryset.filter(
            init_tweet_deleted=False, completed_at__isnull=True
        )

        return qs


class TweetTextCompilation(TwitterMixin, models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
    )
    init_tweet_json = JSONField()
    final_tweet_json = JSONField(
        null=True,
    )
    init_tweet_deleted = models.BooleanField(
        default=False,
    )
    requested_at = models.DateTimeField(
        auto_now_add=True,
    )
    completed_at = models.DateTimeField(
        null=True,
    )
    tweets = ArrayField(
        JSONField(),
    )
    text = models.TextField(
        blank=True,
    )

    def complete(self):
        self.tweets = self.get_tweets()

        self.init_tweet_json['full_text'] = self.init_tweet_json['text']

        self.append(self.init_tweet_json)

        sorted_tweets = sorted(self.tweets, key=lambda k: k['id'])

        self.text = '\n\n'.join([
            i['full_text'].replace('@TweetsToText', '').strip()
            for i in sorted_tweets
        ])

        self.completed_at = timezone.now()

        return self.save()

    def get_tweets(self):
        params = dict(
            user_id=self.user.id_str,
            since_id=self.init_tweet.id_str,
            max_id=self.final_tweet.id_str,
            count=200,
            include_rts=True,
            tweet_mode='extended',
        )

        response = self.twitter_api.request(
            'statuses/user_timeline',
            params,
        )
        response.response.raise_for_status()

        if len(response.json()) > 199:
            pager = TwitterPager(
                self.twitter_api, 'statuses/user_timeline', params
            )
            tweets = []
            for i in pager.get_iterator(wait=3.5):
                tweets.append(i['text'])
        else:
            tweets = response.json()

        return tweets

    def refresh_init_tweet(self):
        try:
            self.init_tweet_json = self.init_tweet.get_from_twitter()
        except HTTPError:
            self.init_tweet_deleted = True

        return self.save()

    def reply_to_init_tweet(self):
        if not settings.TESTING:
            sleep(5)

        status = '@{0} {1}'.format(
            self.user.screen_name, random.choice(constants.replies)
        )
        params = dict(
            status=status,
            in_reply_to_status_id=self.init_tweet_id,
        )

        return self.twitter_api.request('statuses/update', params)

    @property
    def init_tweet(self):
        return Tweet(**self.init_tweet_json)

    @property
    def final_tweet(self):
        return Tweet(**self.final_tweet_json)

    objects = TweetTextCompilationManager()

    class Meta:
        indexes = [
            models.Index(
                fields=['requested_at', ],
                name='requested_at_index',
            ),
            models.Index(
                fields=['completed_at', ],
                name='completed_at_index',
            ),
        ]
