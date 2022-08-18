from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from twitter.apps.core.models import TimeStampedBase, CreatorBase
from twitter.apps.user.models import User


class Follow(TimeStampedBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')


class Tweet(MPTTModel, CreatorBase, TimeStampedBase):
    message = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    retweets = models.PositiveIntegerField(default=0)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        ordering = ['-modified']
