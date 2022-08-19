from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
        tweet_query = Tweet.objects.root_nodes().order_by('-modified')
        if not user.is_anonymous:
            following_users = list(Follow.objects.filter(follower=user).values_list('follower_id', flat=True))
            following_users.append(user.id)
            return tweet_query.filter(creator__id__in=following_users)
        return tweet_query


@login_required
def post_tweet_view(request):
    Tweet.objects.create(message=request.POST.get('message'))
    return redirect('/')
