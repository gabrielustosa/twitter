from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.forms.models import model_to_dict

from twitter.apps.twitter.constants import Action
from twitter.apps.twitter.models import Tweet, TweetAction
from twitter.apps.twitter.objects import TweetManageQuerySet
from utils.tweet import parse_tweet


def home_view(request):
    return render(request, 'twitter/home.html')


class LoadTweetView(ListView):
    template_name = 'twitter/includes/tweet/load_tweet.html'
    model = Tweet
    paginate_by = 5
    context_object_name = 'tweets'

    def get_queryset(self):
        queryset = Tweet.timeline_objects.user_timeline(self.request.user)
        return TweetManageQuerySet(queryset=queryset)


@login_required
def post_tweet_view(request):
    parsed_tweet = parse_tweet(request.POST.get('message'))
    Tweet.objects.create(message=parsed_tweet)
    return redirect('/')


def tweet_view(request, tweet_id):
    tweet_main = get_object_or_404(Tweet, id=tweet_id)
    tweet_ancestors = tweet_main.get_ancestors()
    return render(request, 'twitter/includes/tweet/tweet_view.html', context={
        'tweet_main': tweet_main,
        'tweet_ancestors': tweet_ancestors,
    })


def answer_tweet(request, tweet_id):
    parsed_tweet = parse_tweet(request.POST.get('message'))
    tweet_main = Tweet.objects.get(id=tweet_id)
    tweet = Tweet.objects.create(message=parsed_tweet, parent_id=tweet_id)
    if tweet_main.is_root_node():
        TweetAction.objects.create(tweet_id=tweet_id, action=Action.COMMENT, answer=tweet)
    return tweet_view(request, tweet_id)


class LoadTweetAnswer(ListView):
    template_name = 'twitter/includes/tweet/load_tweet_answer.html'
    model = Tweet
    paginate_by = 5
    context_object_name = 'tweets'

    def get_queryset(self):
        tweet = Tweet.objects.get(id=self.kwargs.get('tweet_id'))
        return tweet.get_children().order_by('-modified')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['twitter_id'] = self.kwargs.get('tweet_id')
        return context


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
