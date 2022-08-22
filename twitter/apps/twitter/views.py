from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from twitter.apps.twitter.models import Tweet
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
    tweet = get_object_or_404(Tweet, id=tweet_id)

    return render(request, 'twitter/includes/tweet/types/tweet_view.html', context={'tweet': tweet})


def answer_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    Tweet.objects.create(message=request.POST.get('message'), parent=tweet)

    return tweet_view(request, tweet_id)


class LoadTweetAnswer(ListView):
    template_name = 'twitter/includes/tweet/load_tweet_answer.html'
    model = Tweet
    paginate_by = 5
    context_object_name = 'tweets_answers'

    def get_queryset(self):
        tweet = Tweet.objects.get(id=self.kwargs.get('tweet_id'))
        return tweet.get_children().order_by('-modified')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['twitter_id'] = self.kwargs.get('tweet_id')
        return context
