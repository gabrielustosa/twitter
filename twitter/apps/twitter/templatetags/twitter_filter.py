from django import template
from django.utils import timezone

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
def parse_tweet(tweet):
    words = [word for word in tweet.split() if word.startswith('#') or word.startswith('@')]

    parsed_tweet = ''
    for index, word_twitter in enumerate(tweet.split()):
        new_word = tweet.split()[index]
        for word in words:
            if word == word_twitter:
                wrapped_word = f'<a href="/teste" class="text-blue-400 hover:underline">{word}</a>'
                new_word = wrapped_word
        parsed_tweet += f'{new_word} '

    return parsed_tweet


@register.filter()
def tweet_ancestors_parsed(tweet):
    ancestors = tweet.get_ancestors(include_self=False)

    two = ancestors[0:2]

    string_format = '<a href="/teste" class="text-blue-400 hover:underline">@{0}</a>'
    ancestors_parsed = ' '.join([string_format.format(tweet.creator.name) for tweet in two])

    if ancestors.count() > 2:
        ancestors_parsed += f' <span class="text-blue-400 hover:underline">e mais {ancestors.count()}</span>'

    return ancestors_parsed
