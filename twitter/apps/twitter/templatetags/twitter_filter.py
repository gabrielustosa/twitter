from django import template
from django.utils import timezone

from utils.profile import get_url_profile as util_get_url_profile

register = template.Library()

DAYS_PER_YEAR = 365
DAYS_PER_MONTH = 30
DAYS_PER_WEEK = 7


@register.filter(is_safe=True)
def date_since(value):
    today = timezone.now().astimezone()
    diff = today - value
    diff_years = int(diff.days / DAYS_PER_YEAR)
    diff_months = int(diff.days / DAYS_PER_MONTH)
    diff_weeks = int(diff.days / DAYS_PER_WEEK)
    diff_map = [
        ("ano", "anos", diff_years,),
        ("mês", "meses", diff_months,),
        ("semana", "semanas", diff_weeks,),
        ("dia", "dias", diff.days,),
    ]
    for parts in diff_map:
        interval, intervals, count = parts
        if count > 1:
            return f"há {count} {intervals}"
        elif count == 1:
            return "Ontem" if interval == "dia" else f"{interval} passada "
    if diff.days == 0:
        hours = diff.total_seconds() / 3600
        if int(hours) > 0:
            return f'{int(hours)}h'
        minutes = diff.total_seconds() / 60
        if int(minutes) > 0:
            return f'{int(minutes)}m'
        seconds = diff.total_seconds()
        return f'{int(seconds)}s'

    else:
        return f"{value:%d %B, %Y}"


@register.filter()
def get_url_profile(name):
    return util_get_url_profile(name)
