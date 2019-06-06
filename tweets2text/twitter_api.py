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
                settings.TWITTER_ACCESS_TOKEN_SECRE,
            )

        return self._twitter_api


class TwitterObject(TwitterMixin):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_from_twitter(self):
        resource_url = '{0}/show/:{1}'.format(
            self.__class__.resource, self.id_str
        )

        return self.twitter_api.request(resource_url)


class Tweet(TwitterObject):
    resource = 'statuses'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = TwitterUser(**self.user)

    @property
    def user_obj(self):
        return self._user_obj

    @property
    def is_actionable_mention(self):
        if self.user.is_follower:
            if self.is_reply:
                if (
                    self.is_self_reply and
                    self.user.as_tweets2text_user.has_pending_compilations
                ):
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
        self._is_self_reply = self.in_reply_to_user_id == self.user['id_str']
        return self._is_self_reply


class TwitterUser(TwitterObject):
    resource = 'users'

    @property
    def is_follower(self):
        try:
            self._follower
        except AttributeError:
            connections = self.get_connections_with_user(
                settings.BOT_ACCOUNT_ID_STR
            )
            self._follower = 'following' in connections

        return self._follower

    def get_connections_with_user(self):
        params = dict(user_id=self.id_str)
        response = self.twitter_api.request(
            'friendships/lookup', params
        )
        connections = response.json()[0]['connections']

        return connections

    @property
    def as_tweets2text_user(self):
        m = apps.get_app_config('admin').get_model('User')
        return m.objects.get(id_str=self.id_str)
