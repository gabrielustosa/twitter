from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

from twitter.apps.twitter.models import Tweet, TweetImage
from utils.profile import get_url_profile as util_get_url_profile

register = template.Library()


@register.filter(is_safe=True)
def date_since(value):
    today = timezone.now().astimezone()
    diff = today - value

    if diff.days == 0:
        hours = diff.total_seconds() / 3600
        if int(hours) > 0:
            return f'{int(hours)}h'
        minutes = diff.total_seconds() / 60
        if int(minutes) > 0:
            return f'{int(minutes)}m'
        seconds = diff.total_seconds()
        return f'{int(seconds)}s'

    if diff.days <= 10:
        return f'{diff.days} d'
    else:
        return f'{value.day} {value.strftime("%b")}'


@register.filter()
def get_url_profile(name):
    return util_get_url_profile(name)


@register.filter()
def format_tweet_numbers(value):
    if value >= 100000:
        return f'{format_tweet_numbers(value / 1000)}K'

    if value >= 10000:
        return f'{value / 1000:.1f}K'

    return value


@register.filter()
def tweet_ancestors_parsed(tweet):
    ancestors = tweet.get_ancestors().order_by('creator').distinct('creator')

    two = ancestors[0:2]

    string_format = '<a href="/user/{0}" class="text-blue-400 hover:underline">@{0}</a>'
    ancestors_parsed = ' '.join([string_format.format(tweet.creator.name) for tweet in two])

    if ancestors.count() > 2:
        ancestors_parsed += f' <span class="text-blue-400 hover:underline">e mais {ancestors.count() - 2}</span>'

    return mark_safe(ancestors_parsed)


@register.filter()
def has_liked(user, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    return tweet.likes.filter(id=user.id).exists()


@register.filter()
def has_retweeted(user, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    return tweet.retweets.filter(id=user.id).exists()


@register.filter()
def is_following(user, follower):
    return user.followers.filter(follower=follower).exists()


@register.filter()
def load_tweet_images(tweet_id):
    images_url = [image.get_absolute_url() for image in TweetImage.objects.filter(tweet_id=tweet_id).all()]
    images_element = [f'<img src="{url}" style="width: 250px;height: 250px; object-fit: cover;">' for url in images_url]

    if len(images_url) == 0:
        return ''

    return mark_safe(f"""
        <div class="grid grid-cols-2 gap-2 py-2">
            {''.join(images_element)}
        </div>
    """)
