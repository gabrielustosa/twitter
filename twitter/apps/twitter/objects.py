from dataclasses import dataclass, field
from datetime import datetime

from django.db.models import QuerySet


@dataclass
class TweetManageQuerySet:
    queryset: QuerySet

    def __len__(self):
        return self.queryset.count()

    def __getitem__(self, item):
        return [Tweet(*item) for item in self.queryset[item]]


@dataclass()
class Tweet:
    id: int
    parent: int
    message: str
    likes: int
    retweets: int
    creator_name: str
    creator_user: str
    modified: datetime
    comments: int
    action: str
    action_user_name: str
    action_user: str
    template: str = field(init=False)

    def __post_init__(self):
        templates = {
            'None': 'twitter/includes/tweet_bases/tweet.html',
            '1': 'twitter/includes/tweet_bases/tweet_retweet.html',
            '2': 'twitter/includes/tweet_bases/tweet_like.html',
            '3': 'twitter/includes/tweet_bases/tweet_comment.html',
        }
        self.template = templates[self.action]
