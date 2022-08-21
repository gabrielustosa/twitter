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
