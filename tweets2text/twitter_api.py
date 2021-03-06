from html import unescape
from django.apps import apps
from django.conf import settings
from TwitterAPI import TwitterAPI


class TwitterMixin(object):

    @property
    def twitter_api(self):
        try:
            self._twitter_api
        except AttributeError:
            self._twitter_api = TwitterAPI(
                settings.TWITTER_CONSUMER_KEY,
                settings.TWITTER_CONSUMER_SECRET,
                settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_TOKEN_SECRET,
            )

        return self._twitter_api


class TwitterObject(TwitterMixin):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        # add id_str if missing (an issue with legacy data?)
        if hasattr(self, 'id') and not hasattr(self, 'id_str'):
            self.id_str = getattr(self, 'id_str', str(self.id))

    def get_from_twitter(self):
        return self.twitter_api.request(self.resource_url)

    @property
    def resource_url(self):
        return '{0}/show/:{1}'.format(self.__class__.resource, self.id_str)


class Tweet(TwitterObject):
    resource = 'statuses'

    @property
    def user_obj(self):
        return TwitterUser(**self.user)

    @property
    def is_actionable_mention(self):
        if self.user_obj.is_follower:
            if self.is_reply:
                t2t_user = self.user_obj.as_tweets2text_user
                if (
                    self.is_self_reply
                    and t2t_user.has_pending_compilation
                ):
                    init_tweet = t2t_user.pending_compilation.init_tweet
                    if init_tweet.id == self.in_reply_to_status_id:
                        is_actionable = False
                    else:
                        is_actionable = True
                else:
                    is_actionable = False
            elif self.is_quote_status or self.is_retweet:
                is_actionable = False
            else:
                is_actionable = True
        else:
            is_actionable = False

        return is_actionable

    @property
    def is_reply(self):
        is_reply = bool(
            self.in_reply_to_status_id_str
        ) or bool(
            self.in_reply_to_status_id
        )

        return is_reply

    @property
    def is_retweet(self):
        self._is_retweet = hasattr(self, 'retweeted_status')
        return self._is_retweet

    @property
    def is_self_reply(self):
        test = self.in_reply_to_user_id_str == self.user_obj.id_str
        return test

    @property
    def urls(self):
        try:
            urls = self.entities['urls']
        except (AttributeError, IndexError, KeyError):
            urls = []

        return urls

    @property
    def user_mentions(self):
        try:
            users = [
                u for u in self.entities['user_mentions']
                if u["screen_name"] != 'TweetsToText'
            ]
        except (AttributeError, IndexError, KeyError):
            users = []

        return users

    def get_formatted_text(self):
        # substitute screen_names for user names, short urls for expanded ones
        text = unescape(self.full_text).replace('@TweetsToText', '')

        for url in self.urls:
            text = text.replace(url['url'], url['expanded_url'])

        for user in self.user_mentions:
            text = text.replace(
                '@%s' % user['screen_name'], user['name']
            )

        return text.strip().replace("  ", " ").replace(" .", ".")

    def get_from_twitter(self):
        return self.twitter_api.request(
            self.resource_url, dict(tweet_mode='extended'),
        )


class TwitterUser(TwitterObject):
    resource = 'users'

    @property
    def is_follower(self):
        try:
            self._is_follower
        except AttributeError:
            connections = self.get_connections_with_bot()
            self._is_follower = 'followed_by' in connections

        return self._is_follower

    def get_connections_with_bot(self):
        params = dict(user_id=self.id_str)
        response = self.twitter_api.request(
            'friendships/lookup', params
        )
        connections = response.json()[0]['connections']

        return connections

    def get_or_create_tweets2text_user(self):
        m = apps.get_app_config('tweets2text').get_model('User')

        try:
            user = m.objects.get(id_str=self.id_str)
        except m.DoesNotExist:
            user = m.objects.create(
                id=self.id,
                id_str=self.id_str,
                name=self.name,
                screen_name=self.screen_name,
                location=self.location,
            )
            created = True
        else:
            created = False

        return user, created

    @property
    def as_tweets2text_user(self):
        m = apps.get_app_config('tweets2text').get_model('User')
        try:
            t2t_user = m.objects.get(id_str=self.id_str)
        except m.DoesNotExist:
            if self.is_follower:
                t2t_user = self.get_or_create_tweets2text_user()[0]
            else:
                raise Exception('No record of Twitter user #%s as follower.')
        return t2t_user
