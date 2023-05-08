from django import template
from modeltranslation.settings import DEFAULT_LANGUAGE
from wagtail_modeltranslation.contextlib import use_language

from ..models import Menu

register = template.Library()


@register.simple_tag()
def get_menu(slug):
    return Menu.objects.get(slug=slug)


@register.simple_tag()
def menu_item_trans_fields(instance, field, language=None):
    """
    Examples:
        {% menu_item_trans_fields instance 'link_url' 'es' %}

    Returns the URL for the page that has the given slug.
    """
    if language and getattr(instance, f'{field}_{language}'):
        attr = getattr(instance, f'{field}_{language}')
    else:
        attr = getattr(instance, f'{field}_{DEFAULT_LANGUAGE}')
    text = text = getattr(instance, attr)
    return text
