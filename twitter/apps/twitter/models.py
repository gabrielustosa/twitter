from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from twitter.apps.core.models import TimeStampedBase, CreatorBase
from twitter.apps.twitter.constants import Action
from twitter.apps.twitter.queryset import TweetQuerySet
from twitter.apps.user.models import User


class Follow(TimeStampedBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')


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


class TweetImage(models.Model):
    image = models.ImageField(upload_to='avatars')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)


class TweetAction(CreatorBase, TimeStampedBase):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    answer = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='answer', null=True)
    action = models.CharField(max_length=2, choices=Action.choices)
