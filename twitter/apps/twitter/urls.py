from django.urls import path

from . import views

app_name = 'twitter'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('tweet/load/', views.LoadTweetsView.as_view(), name='load_tweets'),
    path('tweet/post/', views.post_tweet_view, name='post_tweet'),
]
