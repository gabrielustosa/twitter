from django.db import models
from django.db.models import Value, Q, Count, F, Case, When, Sum
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

        tweet_query = tweet_query.values_list('id').annotate(
            parent=F('parent'),
            message=F('message'),
            likes=Count('likes'),
            retweets=Count('retweets'),
            comments=Count('children'),
            creator_name=F('creator__name'),
            creator_user=F('creator__user'),
            modified=F('modified'),
            action=Value('None'),
            action_creator=Value('None'),
            action_user=Value('None'),
            answer_id=Value(0),
            template=Value('twitter/includes/tweet/types/tweet_timeline.html')
        )

        tweet_action_query = tweet_action_query.values_list('tweet__id').annotate(
            parent=F('tweet__parent'),
            message=F('tweet__message'),
            likes=Count('tweet__likes'),
            retweets=Count('tweet__retweets'),
            comments=Count('tweet__children'),
            creator_name=F('tweet__creator__name'),
            creator_user=F('tweet__creator__user'),
            modified=F('tweet__modified'),
            action=F('action'),
            action_creator=F('creator__name'),
            action_user=F('creator__user'),
            answer_id=F('answer_id'),
            template=Case(
                When(action=Action.RETWEET, then=Value('twitter/includes/tweet/types/tweet_retweet.html')),
                When(action=Action.LIKE, then=Value('twitter/includes/tweet/types/tweet_like.html')),
                When(action=Action.COMMENT, then=Value('twitter/includes/tweet/types/tweet_comment.html')),
            )
        )

        return tweet_query.union(tweet_action_query).order_by('-modified')


class Tweet(MPTTModel, CreatorBase, TimeStampedBase):
    message = models.TextField()
    likes = models.ManyToManyField(
        User,
        related_name='tweets_liked',
        blank=True
    )
    retweets = models.ManyToManyField(
        User,
        related_name='tweets_retweeted',
        blank=True
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    timeline_objects = TweetQuerySet.as_manager()


class TweetAction(CreatorBase, TimeStampedBase):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    answer = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='answer', null=True)
    action = models.CharField(max_length=2, choices=Action.choices)
