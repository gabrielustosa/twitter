from dataclasses import dataclass

from django.db.models import QuerySet, Value, Q, Count, F, Case, When

twitter_values = ('id', 'parent', 'message', 'likes', 'retweets',
                  'comments', 'creator_name', 'creator_user',
                  'modified', 'action', 'action_creator',
                  'action_user', 'answer_id', 'order_date', 'template')


@dataclass
class TweetManageQuerySet:
    queryset: QuerySet

    def __len__(self):
        return self.queryset.count()

    def __getitem__(self, item):
        return [tweet for tweet in self.queryset[item].values(*twitter_values)]


class TweetQuerySet(QuerySet):
    def user_timeline(self, user):
        from twitter.apps.twitter.constants import Action
        from twitter.apps.twitter.models import Tweet, TweetAction

        tweet_query = Tweet.objects.root_nodes()

        if user.is_authenticated:
            following_users = user.following.values_list('user_id')

            tweet_query = tweet_query.filter(Q(creator_id__in=following_users) | Q(creator_id=user.id))
            tweet_action_query = TweetAction.objects.filter(creator_id__in=following_users)

            tweet_action_query = tweet_action_query.values_list('tweet__id').annotate(
                parent=F('tweet__parent'),
                message=F('tweet__message'),
                likes=Count('likes'),
                retweets=Count('tweet__retweets'),
                comments=Count('tweet__children'),
                creator_name=F('tweet__creator__name'),
                creator_user=F('tweet__creator__user'),
                modified=F('tweet__modified'),
                action=F('action'),
                action_creator=F('creator__name'),
                action_user=F('creator__user'),
                answer_id=F('answer_id'),
                order_date=F('created'),
                template=Case(
                    When(action=Action.RETWEET, then=Value('twitter/includes/tweet/types/tweet_retweet.html')),
                    When(action=Action.LIKE, then=Value('twitter/includes/tweet/types/tweet_like.html')),
                    When(action=Action.COMMENT, then=Value('twitter/includes/tweet/types/tweet_comment.html')),
                )
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
            action=Value('Nones'),
            action_creator=Value('None'),
            action_user=Value('Non'),
            answer_id=Value(0),
            order_date=F('created'),
            template=Value('twitter/includes/tweet/types/tweet_timeline.html')
        )

        if user.is_anonymous:
            return tweet_query.order_by('-order_date')

        return tweet_query.order_by('-order_date')
