from braces.views import CsrfExemptMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView
from django.core import serializers

from twitter.apps.twitter.constants import Action
from twitter.apps.twitter.models import Tweet, TweetAction, TweetImage
from twitter.apps.twitter.queryset import TweetManageQuerySet
from twitter.apps.user.models import User
from utils.tweet import parse_tweet


def home_view(request):
    return render(request, 'twitter/home.html')


class LoadTweetBase(ListView):
    model = Tweet
    paginate_by = 5
    context_object_name = 'tweets'


class LoadTweetView(LoadTweetBase):
    template_name = 'twitter/includes/tweet/load_tweet.html'

    def get_queryset(self):
        queryset = Tweet.timeline_objects.user_timeline(self.request.user)
        return TweetManageQuerySet(queryset=queryset)


class LoadTweetAnswer(LoadTweetBase):
    template_name = 'twitter/includes/tweet/load_tweet_answer.html'

    def get_queryset(self):
        tweet = Tweet.objects.get(id=self.kwargs.get('tweet_id'))
        return tweet.get_children().order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['twitter_id'] = self.kwargs.get('tweet_id')
        return context


class LoadTweetResults(TemplateView):
    template_name = 'twitter/includes/tweet/load_search_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        term = self.request.GET.get('term')

        query = Tweet.objects.filter(message__icontains=term).annotate(comments=Count('children'))

        context['tweets'] = query
        context['term'] = term
        context['total'] = query.count

        return context


class LoadUserTweets(LoadTweetBase):
    template_name = 'twitter/includes/tweet/load_user_tweets.html'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Tweet.objects.filter(creator__id=user_id).annotate(comments=Count('children'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['user_id'] = self.kwargs.get('user_id')
        return context


@login_required
def post_tweet_view(request):
    parsed_tweet = parse_tweet(request.POST.get('message'))
    tweet = Tweet.objects.create(message=parsed_tweet)

    images = request.FILES.getlist(key='images')
    [TweetImage.objects.create(image=image, tweet=tweet) for image in images[0:4]]

    return redirect('/')


def tweet_view(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    tweet_ancestors = tweet.get_ancestors()
    return render(request, 'twitter/includes/tweet/tweet_view.html', context={
        'tweet': tweet,
        'tweet_ancestors': tweet_ancestors,
    })


def answer_tweet(request, tweet_id):
    parsed_tweet = parse_tweet(request.POST.get('message'))
    tweet_main = Tweet.objects.get(id=tweet_id)
    tweet = Tweet.objects.create(message=parsed_tweet, parent_id=tweet_id)
    if tweet_main.is_root_node():
        TweetAction.objects.create(tweet_id=tweet_id, action=Action.COMMENT, answer=tweet)
    return tweet_view(request, tweet_id)


def get_tweet(request, tweet_id):
    tweet = Tweet.objects.filter(id=tweet_id).annotate(comments=Count('children')).first()
    return render(request, 'twitter/includes/tweet/types/tweet_normal.html', context={'tweet': tweet})


def like_tweet_view(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
        if tweet.is_root_node():
            TweetAction.objects.filter(tweet_id=tweet_id, action=Action.LIKE).delete()
    else:
        tweet.likes.add(request.user)
        if tweet.is_root_node():
            TweetAction.objects.create(tweet_id=tweet_id, action=Action.LIKE)

    return render(request, 'twitter/includes/tweet/partials/tweet_like.html',
                  context={'tweet_likes': tweet.likes.count(), 'tweet': tweet})


def retweet_tweet_view(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    if tweet.retweets.filter(id=request.user.id).exists():
        tweet.retweets.remove(request.user)
        if tweet.is_root_node():
            TweetAction.objects.filter(tweet_id=tweet_id, action=Action.RETWEET).delete()
    else:
        tweet.retweets.add(request.user)
        if tweet.is_root_node():
            TweetAction.objects.create(tweet_id=tweet_id, action=Action.RETWEET)

    return render(request, 'twitter/includes/tweet/partials/tweet_retweet.html',
                  context={'tweet_retweets': tweet.retweets.count(), 'tweet': tweet})


def user_view(request, user):
    user = get_object_or_404(User, user__iexact=user)
    return render(request, 'twitter/includes/user/profile.html', context={'twitter_user': user})


