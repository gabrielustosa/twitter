from rest_framework.routers import SimpleRouter

from twitter.apps.twitter.api import views

tweet_api_v1_router = SimpleRouter()
tweet_api_v1_router.register(
    'twitter/api/v1',
    views.TweetAPIViewSet
)

urlpatterns = tweet_api_v1_router.urls
