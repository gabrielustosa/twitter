from rest_framework import serializers

from twitter.apps.twitter.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(
        source='likes.count',
        read_only=True,
    )
    retweets_count = serializers.IntegerField(
        source='retweets.count',
        read_only=True,
    )
    comments_count = serializers.IntegerField(
        source='children.count',
        read_only=True,
    )

    class Meta:
        model = Tweet
        fields = [
            'id',
            'message',
            'creator',
            'likes_count',
            'retweets_count',
            'comments_count',
        ]
