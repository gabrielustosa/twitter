from dataclasses import dataclass

from django.db.models import QuerySet

twitter_values = ('id', 'parent', 'message', 'likes', 'retweets',
                  'comments', 'creator_name', 'creator_user',
                  'modified', 'action', 'action_creator',
                  'action_user', 'answer_id', 'template')


@dataclass
class TweetManageQuerySet:
    queryset: QuerySet

    def __len__(self):
        return self.queryset.count()

    def __getitem__(self, item):
        return [tweet for tweet in self.queryset[item].values(*twitter_values)]
