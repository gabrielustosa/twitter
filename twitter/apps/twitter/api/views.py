from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from twitter.apps.twitter.api.serializer import TweetSerializer
from twitter.apps.twitter.models import Tweet


class TweetAPIViewSet(ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'options', 'head']
