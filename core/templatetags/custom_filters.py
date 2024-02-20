from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter(name='time_ago')
def time_ago(value):
    if value is None:
        return 'N/A'

    now = timezone.now()
    delta = now - value

    if delta < timedelta(minutes=1):
        return 'just now'
    elif delta < timedelta(hours=1):
        minutes = delta.seconds // 60
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    elif delta < timedelta(days=1):
        hours = delta.seconds // 3600
        return f'{hours} hour{"s" if hours != 1 else ""} ago'
    else:
        days = delta.days
        return f'{days} day{"s" if days != 1 else ""} ago'
