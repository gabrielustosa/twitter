from django.shortcuts import render
from django.views.generic import ListView

from twitter.apps.twitter.models import Tweet, Follow


def home_view(request):
    return render(request, 'twitter/home.html')


class LoadTweetsView(ListView):
    template_name = 'twitter/includes/tweet.html'
    model = Tweet
    paginate_by = 5
    context_object_name = 'tweets'

    def get_queryset(self):
        user = self.request.user
        tweet_query = Tweet.objects.filter(parent=None)
        if not user.is_anonymous:
            following_users = Follow.objects.filter(follower=user).values_list('follower_id', flat=True)
            return tweet_query.filter(creator__in=[following_users])
        return tweet_query

    def get_paginate_by(self, queryset):
        return self.request.GET.get('page', self.paginate_by)
