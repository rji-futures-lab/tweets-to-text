import re
from django.contrib.sites.models import Site
from django.db import IntegrityError
from django.utils import timezone
from tweets2text.models import (
    AccountActivity, FollowHistory, TweetTextCompilation
)
from zappa.asynchronous import task
from tweets2text.twitter_api import Tweet, TwitterUser


@task()
def handle_account_activity(account_activity_id):

    activity = AccountActivity.objects.get(id=account_activity_id)
    if activity.processing_started_at:
        return
    else:
        activity.processing_started_at = timezone.now()
        activity.save()

    for follow in activity.follow_events:
        follower = TwitterUser(**follow.source)

        user, created = follower.get_or_create_tweets2text_user()

        if created:
            user.send_welcome_dm()
        else:
            user.last_follow_at = timezone.now()
            user.save()
            user.send_dm('Welcome back!')

        user.follow_history.create(event_json=follow.__dict__)

    for unfollow in activity.unfollow_events:
        unfollower = TwitterUser(**unfollow.source)
        try:
            FollowHistory.objects.create(
                user_id=unfollower.id,
                event_json=unfollow.__dict__
            )
        except IntegrityError:
            pass

    for tweet in activity.tweet_create_events:
        if tweet.is_actionable_mention:
            user = tweet.user_obj.as_tweets2text_user

            if user.has_pending_compilation:
                user.pending_compilation.refresh_init_tweet()

            if user.has_pending_compilation:
                pending_compilation = user.pending_compilation
                pending_compilation.final_tweet_json = tweet.__dict__
                pending_compilation.save()
                pending_compilation.complete()

                url = 'https://%s%s' % (
                    Site.objects.get_current().domain,
                    pending_compilation.get_absolute_url()
                )
                user.send_dm(url)

            else:
                new_compilation = TweetTextCompilation.objects.create(
                    user=user, init_tweet_json=tweet.__dict__
                )
                new_compilation.reply_to_init_tweet()

    for dm in activity.direct_message_events:
        if dm.type == 'message_create':
            message_data = dm.message_create['message_data']
            try:
                url = message_data["entities"]["urls"][0]["expanded_url"]
            except (KeyError, IndexError):
                pass
            else:
                tweet_url_regex = re.compile(
                    r'https://twitter\.com/.+/status/(?P<tweet_id>\d+)'
                )
                match = tweet_url_regex.match(url)
                if match:
                    tweet_id = match.groupdict()['tweet_id']
                    response = Tweet(id=tweet_id).get_from_twitter()
                    if response.response.ok:
                        init_tweet = response.json()
                        sender = TwitterUser(**init_tweet['user'])
                        if sender.is_follower:
                            user = sender.get_or_create_tweets2text_user()[0]
                            compilation = user.compilations.create(
                                init_tweet_json=init_tweet
                            )
                            compilation.complete()
                            url = 'https://%s%s' % (
                                Site.objects.get_current().domain,
                                compilation.get_absolute_url()
                            )
                            user.send_dm(url)

    activity.processing_completed_at = timezone.now()

    return activity.save()
