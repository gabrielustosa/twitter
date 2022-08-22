from django.urls import path

from . import views

app_name = 'twitter'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('tweet/load/', views.LoadTweetView.as_view(), name='load_tweets'),
    path('tweet/post/', views.post_tweet_view, name='post_tweet'),
    path('tweet/<int:tweet_id>/', views.tweet_view, name='view_tweet'),
    path('tweet/answer/<int:tweet_id>/', views.answer_tweet, name='answer_tweet'),
    path('tweet/load/answers/<int:tweet_id>/', views.LoadTweetAnswer.as_view(), name='load_answers'),
    path('tweet/get/<int:tweet_id>/', views.get_tweet, name='get_tweet'),
]
