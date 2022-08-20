from django.db import models
from django.db.models import Value, Q, Count, F
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from twitter.apps.core.models import TimeStampedBase, CreatorBase
from twitter.apps.twitter.constants import Action
from twitter.apps.user.models import User


class Follow(TimeStampedBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')


class TweetQuerySet(models.QuerySet):
    def user_timeline(self, user):
        tweet_query = Tweet.objects.root_nodes()
        tweet_action_query = TweetAction.objects

        if user.is_authenticated:
            following_users = Follow.objects.filter(follower=user).values_list('follower_id', flat=True)

            tweet_query = tweet_query.filter(Q(creator__id__in=following_users) | Q(creator__id=user.id))
            tweet_action_query = tweet_action_query.filter(
                Q(tweet__creator__id__in=following_users) | Q(creator__id=user.id)
            )

        tweet_query = tweet_query.values_list(
            'id',
            'parent',
            'message',
            'likes',
            'retweets',
            'creator__name',
            'creator__twitter_user',
            'modified',
        ).annotate(total_coments=Count('children'), col_1=Value('None'), col_2=Value('None'), col_3=Value('None'))

        tweet_action_query = tweet_action_query.values_list(
            'tweet__id',
            'tweet__parent',
            'tweet__message',
            'tweet__likes',
            'tweet__retweets',
            'tweet__creator__name',
            'tweet__creator__twitter_user',
            'modified',
        ).annotate(total_coments=Count('tweet__children'), action=F('action'), creator_name=F('creator__name'),
                   creator_user=F('creator__twitter_user'))

        return tweet_query.union(tweet_action_query).order_by('-modified')


class Tweet(MPTTModel, CreatorBase, TimeStampedBase):
    message = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    retweets = models.PositiveIntegerField(default=0)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    timeline_objects = TweetQuerySet.as_manager()


class TweetAction(CreatorBase, TimeStampedBase):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    action = models.CharField(max_length=2, choices=Action.choices)
