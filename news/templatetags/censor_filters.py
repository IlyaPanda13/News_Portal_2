from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

CENSORED_WORDS = [
    'редиска',
    'плохое',
    'запрещенное',
]


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        return value

    words = value.split()
    result = []

    for word in words:
        lower_word = word.lower()
        if any(censored in lower_word for censored in CENSORED_WORDS):
            censored_word = '*' * len(word)
            result.append(censored_word)
        else:
            result.append(word)

    return mark_safe(' '.join(result))