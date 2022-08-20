from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView

from twitter.apps.twitter.models import Tweet
from twitter.apps.twitter.objects import TweetManageQuerySet


def home_view(request):
    return render(request, 'twitter/home.html')


class LoadTweetView(ListView):
    template_name = 'twitter/includes/tweet.html'
    model = Tweet
    paginate_by = 5
    context_object_name = 'tweets'

    def get_queryset(self):
        queryset = Tweet.timeline_objects.user_timeline(self.request.user)
        return TweetManageQuerySet(queryset=queryset)


@login_required
def post_tweet_view(request):
    Tweet.objects.create(message=request.POST.get('message'))
    return redirect('/')
