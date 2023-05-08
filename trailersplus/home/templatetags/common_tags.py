from string import Template
from posixpath import split
from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
import time
import re

register = template.Library()


@register.filter
def one_more(_1, _2):
    return _1, _2


@register.filter
def add_store(_1_2, _3):
    name, state = _1_2
    store_name_template = re.compile(r'(&lt;|<)\s?store\s?(&gt;|>)')
    if state:
        text = store_name_template.sub(f'{name}, {state}', str(_3))
    else:
        text = store_name_template.sub(f'{name}', str(_3))
    return text

@register.simple_tag(takes_context=True)
def string_substitution(context, value, **kwargs):
    kwargs = {**context.__dict__['dicts'][1], **kwargs}
    substitution = Template(value).safe_substitute(**kwargs)
    return ' '.join(word for word in substitution.split(' ') if not word.startswith('$'))

@register.filter
def add_phone(text, phone):
    phone_template = re.compile(r'(&lt;|<)\s?phone\s?(&gt;|>)')
    return phone_template.sub(f'<a href="tel:+1{phone}">{phone}</a>', str(text))


@register.filter
def locations_count(text, quantity):
    count_template = re.compile(r'(&lt;|<)\s?count\s?(&gt;|>)')
    trailers_template = re.compile(r'(&lt;|<)\s?trailers_count\s?(&gt;|>)')
    text = count_template.sub(str(quantity), text)
    text = trailers_template.sub(str(quantity*100), text)
    return text


@register.filter
def location_slug(text, slug):
    if text is None:
        return None
    slug_template = re.compile(r'(&lt;|<)\s?location_slug\s?(&gt;|>)')
    return slug_template.sub(slug, text)


@register.filter
def hyphen_to_space(text: str) -> str:
    return text.replace('_', ' ')


# @register.filter
# def fix_location_slug(location):
#     split_location = location.split(" ")
#     return "_".join(split_location)
