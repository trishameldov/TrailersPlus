import re
from collections import Counter, deque, namedtuple
from datetime import date, timedelta
from sre_parse import State
from string import Template
from urllib.parse import urlparse

import requests
from api.models import ServiceReviews
from api.utils import path_img
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection, models
from django.db.models import Max, Min, Prefetch, Q
from django.db.models.functions import Now
from django.shortcuts import Http404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import get_language
from home.models import Footer, Header, Partners
from menus.models import MainMenu
from product.models import (Category, CategoryMap, Location, Trailer,
                            TrailerTranslation, Image360)
from sitemaps.inventory import dictfetchall
from streams import blocks as common_blocks
from streams.splitted_blocks.commerce_blocks import (category_blocks,
                                                     detail_page_blocks,
                                                     inventory_blocks,
                                                     my_store_blocks)
from trailersplus.settings import TRUSTPILOT_API_KEY, TRUSTPILOT_BUSINESS_UNIT
from trailersplus.utils.decorators import (additional_context,
                                           define_user_location)
from trailersplus.utils.objects import multiple_q
from wagtail.admin.edit_handlers import (BaseChooserPanel, FieldPanel,
                                         MultiFieldPanel, PageChooserPanel,
                                         StreamFieldPanel)
from wagtail.contrib.routable_page.models import RoutablePage, route
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
# Utils
from wagtail.core.url_routing import RouteResult
from wagtail.snippets.models import register_snippet

from .templatetags.product_tags import extend_title


def serialize_location(location, request, state_slug=''):
    store_trailers = cache.get(f'{location.store_id}-trailers', None)
    if store_trailers is None:
        store_trailers_qs = get_store_trailers(location, state_slug)
        store_trailers = {
            "id": location.store_id,
            "state": location.state,
            "full_state": location.get_state_display(),
            "city": location.store_city,
            "phone": location.store_phone,
            "slug": location.get_slug(),
            "city_name": location.get_city_name(),
            "location_instance": location,
            "map_url": location.store_map_url,
            "store_trailers": store_trailers_qs,
            "count": int(store_trailers_qs.count()),
            "podium_id": location.podium_id,
            "podium_number": location.podium_text_number,
        }
        cache.set(f'{location.store_id}-trailers', store_trailers, 3600 / 4)
    request.session['user_location'] = location.store_id
    request.session.modified = True
    return store_trailers

def get_title_formatting_kwargs(context, request=None):
    if not request:
        request = context['request']
    kwargs = {}
    kwargs['city'] = request.location['city_name']
    kwargs['state'] = request.location["full_state"]
    if context.get('category'):
        kwargs['category'] = context.get('category')
    if context.get('sub_category'):
        kwargs['sub_category'] = sub_category_size(context.get('sub_category'))
    if context.get('product'):
        kwargs['vin'] = context["product"]['common'].vin    
    return kwargs

def build_user_formatted_strings(request, context, usr_string):
    substitution = Template(usr_string).safe_substitute(get_title_formatting_kwargs(context, request))
    return ' '.join(word for word in substitution.split(' ') if not word.startswith('$'))


def get_store_trailers(store, state_slug=False):
    base_qs = Trailer.objects.filter(
            Q(status__lt=150) | Q(sale_date__gte=(date.today() - timedelta(days=7)))
        )
    if not state_slug:
        return base_qs.filter(store=store)
    else:
        return base_qs.filter_state_choices('store__state', state_slug)


def sql_executor(sql, **kwargs):
    with connection.cursor() as cursor:
        cursor.execute(sql, kwargs)
        row = namedtuplefetchall(cursor)
    return row


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_store_trailers_sql(store, lang='EN'):
    sql = """
        SELECT
            DISTINCT cat.slug,
            COUNT(prod.*),cat.pictures,
            MIN(prod.sale_price),
            cat.description
        FROM product_trailer prod
        INNER JOIN product_trailertranslation trans ON prod.vin = trans.trailer_id
        INNER JOIN product_Category cat ON prod.category_id = cat.id
        INNER JOIN product_CategoryMap cm ON cm.id = cat.category_map_id
        WHERE prod.store_id = %(store)s
            AND (
                prod.status = 100
                OR prod.status = 120
                OR (
                        prod.status = 150
                        AND CURRENT_DATE - prod.sale_date <= 7
                    )
            )
            AND trans.language = %(lang)s
        GROUP BY cat.description, cat.pictures, cat.slug
        ORDER BY MIN(prod.sale_price) ASC
    """
    return sql_executor(sql, **{'store': store, 'lang': lang})


def count_store_trailers_sql(store, lang='EN'):
    sql = """
        SELECT
            COUNT(prod.*)
        FROM product_trailer prod
        INNER JOIN product_trailertranslation trans ON prod.vin = trans.trailer_id
        INNER JOIN product_Category cat ON prod.category_id = cat.id
        INNER JOIN product_CategoryMap cm ON cm.id = cat.category_map_id
        WHERE prod.store_id = %(store)s
            AND (
                prod.status = 100
                OR prod.status = 120
                OR (
                        prod.status = 150
                        AND CURRENT_DATE - prod.sale_date <= 7
                    )
            )
            AND trans.language = %(lang)s
        ORDER BY MIN(prod.sale_price) ASC
    """
    return sql_executor(sql, **{'store': store, 'lang': lang})[0].count


def _get_types_filter(store: Location, query: Trailer.objects, count: bool = False):
    result = cache.get(f'{store.pk}_filters_count_{get_language()}', None)
    if result is None:
        if get_language() == 'es':
            result = [
                [
                    'Carga',
                    {
                        'index': 1,
                        'slug': 'Cargo',
                        'sub': [
                            {'Enc4': {
                                'count': query.get_trailers_per_subcategory('Enc4').count(),
                                'index': 1,
                                'web_category': 'Enc4',
                                'slug': '4-Wide-Cargo-Trailers',
                                'verbose': '4\' Carga'
                            }},
                            {'Enc5': {
                                'count': query.get_trailers_per_subcategory('Enc5').count(),
                                'index': 2,
                                'web_category': 'Enc5',
                                'slug': '5-Wide-Cargo-Trailers',
                                'verbose': '5\' Carga'
                            }},
                            {'Enc6': {
                                'count': query.get_trailers_per_subcategory('Enc6').count(),
                                'index': 3,
                                'web_category': 'Enc6',
                                'slug': '6-Wide-Cargo-Trailers',
                                'verbose': '6\' Carga'
                            }},
                            {'Enc6TA': {
                                'count': query.get_trailers_per_subcategory('Enc6TA').count(),
                                'index': 4,
                                'web_category': 'Enc6TA',
                                'slug': '6-Wide-Tandem-Cargo-Trailers',
                                'verbose': '6\' Tandem Carga'
                            }},
                            {'Enc7': {
                                'count': query.get_trailers_per_subcategory('Enc7').count(),
                                'index': 5,
                                'web_category': 'Enc7',
                                'slug': '7-Wide-Cargo-Trailers',
                                'verbose': '7\' Carga'
                            }},
                            {'Enc102': {
                                'count': query.get_trailers_per_subcategory('Enc102').count(),
                                'index': 6,
                                'web_category': 'Enc102',
                                'slug': '8-5-Wide-Cargo-Trailers',
                                'verbose': '8.5\' Carga'
                            }},
                        ]
                    }
                ],
                [
                    'Utilitario',
                    {
                        'index': 2,
                        'slug': 'Utility',
                        'sub': [
                            {'Flt4': {
                                'count': query.get_trailers_per_subcategory('Flt4').count(),
                                'index': 8,
                                'web_category': 'Flt4',
                                'slug': '4-Wide-Utility-Trailers',
                                'verbose': '4\' Utilitario'
                            }},
                            {'Flt5': {
                                'count': query.get_trailers_per_subcategory('Flt5').count(),
                                'index': 9,
                                'web_category': 'Flt5',
                                'slug': '5-Wide-Utility-Trailers',
                                'verbose': '5\' Utilitario'
                            }},
                            {'Flt6': {
                                'count': query.get_trailers_per_subcategory('Flt6').count(),
                                'index': 10,
                                'web_category': 'Flt6',
                                'slug': '6-Wide-Utility-Trailers',
                                'verbose': '6\' Utilitario'
                            }},
                            {'Flt6TA': {
                                'count': query.get_trailers_per_subcategory('Flt6TA').count(),
                                'index': 11,
                                'web_category': 'Flt6TA',
                                'slug': '6-Wide-Tandem-Utility-Trailers',
                                'verbose': '6\' Tandem Utilitario'
                            }},
                            {'Flt7': {
                                'count': query.get_trailers_per_subcategory('Flt7').count(),
                                'index': 12,
                                'web_category': 'Flt7',
                                'slug': '7-Wide-Utility-Trailers',
                                'verbose': '7\' Utilitario'
                            }},
                            {'Flt7TA': {
                                'count': query.get_trailers_per_subcategory('Flt7TA').count(),
                                'index': 13,
                                'web_category': 'Flt7TA',
                                'slug': '7-Wide-Tandem-Utility-Trailers',
                                'verbose': '7\' Tandem Utilitario'
                            }},
                            {'Flt8': {
                                'count': query.get_trailers_per_subcategory('Flt8').count(),
                                'index': 14,
                                'web_category': 'Flt8',
                                'slug': '8-5-Wide-Utility-Trailers',
                                'verbose': '8.5\' Utilitario'
                            }},
                        ]
                    }
                ],
                [
                    'Porta vehiculos',
                    {
                        'index': 3,
                        'slug': 'Hauler',
                        'sub': [
                            {'EncCC': {
                                'count': query.get_trailers_per_subcategory('EncCC').count(),
                                'index': 15,
                                'web_category': 'EncCC',
                                'slug': 'Enclosed-Car-Haulers',
                                'verbose': 'Cerrado Porta vehiculos'
                            }},
                            {'FltCC': {
                                'count': query.get_trailers_per_subcategory('FltCC').count(),
                                'index': 16,
                                'web_category': 'FltCC',
                                'slug': 'Flatbed-Car-Haulers',
                                'verbose': 'Plano Porta vehiculos'
                            }},
                        ]
                    }
                ],
                [
                    'Nieve /ATV',
                    {
                        'index': 4,
                        'slug': 'ATV',
                        'sub': [
                            {'EncATV': {
                                'count': query.get_trailers_per_subcategory('EncATV').count(),
                                'index': 17,
                                'web_category': 'EncATV',
                                'slug': 'Enclosed-ATV-Snowmobile-Trailers',
                                'verbose': 'Cerrado ATV'
                            }},
                            {'FltATV': {
                                'count': query.get_trailers_per_subcategory('FltATV').count(),
                                'index': 18,
                                'web_category': 'FltATV',
                                'slug': 'Flatbed-ATV-Snowmobile-Trailers',
                                'verbose': 'Plano ATV'
                            }},
                        ]
                    }
                ],
                [
                    'Volteo',
                    {
                        'index': 5,
                        'slug': 'Dump',
                        'sub': [
                            {'Dump5': {
                                'count': query.get_trailers_per_subcategory('Dump5').count(),
                                'index': 19,
                                'web_category': 'Dump5',
                                'slug': '5-Wide-Dump-Trailers',
                                'verbose': '5\' Volteo'
                            }},
                            {'Dump6': {
                                'count': query.get_trailers_per_subcategory('Dump6').count(),
                                'index': 20,
                                'web_category': 'Dump6',
                                'slug': '6-Wide-Dump-Trailers',
                                'verbose': '6\' Volteo'
                            }},
                            {'Dump7': {
                                'count': query.get_trailers_per_subcategory('Dump7').count(),
                                'index': 21,
                                'web_category': 'Dump7',
                                'slug': '7-Wide-Dump-Trailers',
                                'verbose': '7\' Volteo'
                            }},
                        ]
                    }
                ],
                [
                    'Equipo',
                    {
                        'index': 6,
                        'slug': 'Equipment',
                        'sub': [
                            {'Eqp6': {
                                'count': query.get_trailers_per_subcategory('Eqp6').count(),
                                'index': 23,
                                'web_category': 'Eqp6',
                                'slug': '6-Wide-Equipment-Trailers',
                                'verbose': '6\' Equipo'
                            }},
                            {'Eqp7': {
                                'count': query.get_trailers_per_subcategory('Eqp7').count(),
                                'index': 24,
                                'web_category': 'Eqp7',
                                'slug': '7-Wide-Equipment-Trailers',
                                'verbose': '7\' Equipo'
                            }},
                            {'Eqp8': {
                                'count': query.get_trailers_per_subcategory('Eqp8').count(),
                                'index': 25,
                                'web_category': 'Eqp8',
                                'slug': '8-5-Wide-Equipment-Trailers',
                                'verbose': '8.5\' Equipo'
                            }},
                        ]
                    }
                ],
                ['Cuello de cisne', {
                    'index': 7,
                    'slug': 'Gooseneck',
                    'sub': [
                        {'Gooseneck': {
                            'count': query.get_trailers_per_subcategory('EqpGN').count(),
                            'index': 26,
                            'web_category': 'EqpGN',
                            'slug': 'Cuello de cisne',
                            'verbose': 'Cuello de cisne'
                        }},
                    ]
                }]
            ]
        else:
            result = [
                [
                    'Cargo',
                    {
                        'index': 1,
                        'slug': 'Cargo',
                        'sub': [
                            {'Enc4': {
                                'count': query.get_trailers_per_subcategory('Enc4').count(),
                                'index': 1,
                                'web_category': 'Enc4',
                                'slug': '4-Wide-Cargo-Trailers',
                                'verbose': '4\' Cargo'
                            }},
                            {'Enc5': {
                                'count': query.get_trailers_per_subcategory('Enc5').count(),
                                'index': 2,
                                'web_category': 'Enc5',
                                'slug': '5-Wide-Cargo-Trailers',
                                'verbose': '5\' Cargo'
                            }},
                            {'Enc6': {
                                'count': query.get_trailers_per_subcategory('Enc6').count(),
                                'index': 3,
                                'web_category': 'Enc6',
                                'slug': '6-Wide-Cargo-Trailers',
                                'verbose': '6\' Cargo'
                            }},
                            {'Enc6TA': {
                                'count': query.get_trailers_per_subcategory('Enc6TA').count(),
                                'index': 4,
                                'web_category': 'Enc6TA',
                                'slug': '6-Wide-Tandem-Cargo-Trailers',
                                'verbose': '6\' Tandem Cargo'
                            }},
                            {'Enc7': {
                                'count': query.get_trailers_per_subcategory('Enc7').count(),
                                'index': 5,
                                'web_category': 'Enc7',
                                'slug': '7-Wide-Cargo-Trailers',
                                'verbose': '7\' Cargo'
                            }},
                            {'Enc102': {
                                'count': query.get_trailers_per_subcategory('Enc102').count(),
                                'index': 6,
                                'web_category': 'Enc102',
                                'slug': '8-5-Wide-Cargo-Trailers',
                                'verbose': '8.5\' Cargo'
                            }},
                        ]
                    }
                ],
                [
                    'Utility',
                    {
                        'index': 2,
                        'slug': 'Utility',
                        'sub': [
                            {'Flt4': {
                                'count': query.get_trailers_per_subcategory('Flt4').count(),
                                'index': 8,
                                'web_category': 'Flt4',
                                'slug': '4-Wide-Utility-Trailers',
                                'verbose': '4\' Utility'
                            }},
                            {'Flt5': {
                                'count': query.get_trailers_per_subcategory('Flt5').count(),
                                'index': 9,
                                'web_category': 'Flt5',
                                'slug': '5-Wide-Utility-Trailers',
                                'verbose': '5\' Utility'
                            }},
                            {'Flt6': {
                                'count': query.get_trailers_per_subcategory('Flt6').count(),
                                'index': 10,
                                'web_category': 'Flt6',
                                'slug': '6-Wide-Utility-Trailers',
                                'verbose': '6\' Utility'
                            }},
                            {'Flt6TA': {
                                'count': query.get_trailers_per_subcategory('Flt6TA').count(),
                                'index': 11,
                                'web_category': 'Flt6TA',
                                'slug': '6-Wide-Tandem-Utility-Trailers',
                                'verbose': '6\' Tandem Utility'
                            }},
                            {'Flt7': {
                                'count': query.get_trailers_per_subcategory('Flt7').count(),
                                'index': 12,
                                'web_category': 'Flt7',
                                'slug': '7-Wide-Utility-Trailers',
                                'verbose': '7\' Utility'
                            }},
                            {'Flt7TA': {
                                'count': query.get_trailers_per_subcategory('Flt7TA').count(),
                                'index': 13,
                                'web_category': 'Flt7TA',
                                'slug': '7-Wide-Tandem-Utility-Trailers',
                                'verbose': '7\' Tandem Utility'
                            }},
                            {'Flt8': {
                                'count': query.get_trailers_per_subcategory('Flt8').count(),
                                'index': 14,
                                'web_category': 'Flt8',
                                'slug': '8-5-Wide-Utility-Trailers',
                                'verbose': '8.5\' Utility'
                            }},
                        ]
                    }
                ],
                [
                    'Car Hauler',
                    {
                        'index': 3,
                        'slug': 'Hauler',
                        'sub': [
                            {'EncCC': {
                                'count': query.get_trailers_per_subcategory('EncCC').count(),
                                'index': 15,
                                'web_category': 'EncCC',
                                'slug': 'Enclosed-Car-Haulers',
                                'verbose': 'Enclosed Car Hauler'
                            }},
                            {'FltCC': {
                                'count': query.get_trailers_per_subcategory('FltCC').count(),
                                'index': 16,
                                'web_category': 'FltCC',
                                'slug': 'Flatbed-Car-Haulers',
                                'verbose': 'Flatbed Car Hauler'
                            }},
                        ]
                    }
                ],
                [
                    'Snow /ATV',
                    {
                        'index': 4,
                        'slug': 'ATV',
                        'sub': [
                            {'EncATV': {
                                'count': query.get_trailers_per_subcategory('EncATV').count(),
                                'index': 17,
                                'web_category': 'EncATV',
                                'slug': 'Enclosed-ATV-Snowmobile-Trailers',
                                'verbose': 'Enclosed ATV'
                            }},
                            {'FltATV': {
                                'count': query.get_trailers_per_subcategory('FltATV').count(),
                                'index': 18,
                                'web_category': 'FltATV',
                                'slug': 'Flatbed-ATV-Snowmobile-Trailers',
                                'verbose': 'Flatbed ATV'
                            }},
                        ]
                    }
                ],
                [
                    'Dump',
                    {
                        'index': 5,
                        'slug': 'Dump',
                        'sub': [
                            {'Dump5': {
                                'count': query.get_trailers_per_subcategory('Dump5').count(),
                                'index': 19,
                                'web_category': 'Dump5',
                                'slug': '5-Wide-Dump-Trailers',
                                'verbose': '5\' Dump'
                            }},
                            {'Dump6': {
                                'count': query.get_trailers_per_subcategory('Dump6').count(),
                                'index': 20,
                                'web_category': 'Dump6',
                                'slug': '6-Wide-Dump-Trailers',
                                'verbose': '6\' Dump'
                            }},
                            {'Dump7': {
                                'count': query.get_trailers_per_subcategory('Dump7').count(),
                                'index': 21,
                                'web_category': 'Dump7',
                                'slug': '7-Wide-Dump-Trailers',
                                'verbose': '7\' Dump'
                            }},
                        ]
                    }
                ],
                [
                    'Equipment',
                    {
                        'index': 6,
                        'slug': 'Equipment',
                        'sub': [
                            {'Eqp6': {
                                'count': query.get_trailers_per_subcategory('Eqp6').count(),
                                'index': 23,
                                'web_category': 'Eqp6',
                                'slug': '6-Wide-Equipment-Trailers',
                                'verbose': '6\' Equipment'
                            }},
                            {'Eqp7': {
                                'count': query.get_trailers_per_subcategory('Eqp7').count(),
                                'index': 24,
                                'web_category': 'Eqp7',
                                'slug': '7-Wide-Equipment-Trailers',
                                'verbose': '7\' Equipment'
                            }},
                            {'Eqp8': {
                                'count': query.get_trailers_per_subcategory('Eqp8').count(),
                                'index': 25,
                                'web_category': 'Eqp8',
                                'slug': '8-5-Wide-Equipment-Trailers',
                                'verbose': '8.5\' Equipment'
                            }},
                        ]
                    }
                ],
                ['Gooseneck', {
                    'index': 7,
                    'slug': 'Gooseneck',
                    'sub': [
                        {'Gooseneck': {
                            'count': query.get_trailers_per_subcategory('EqpGN').count(),
                            'index': 26,
                            'web_category': 'EqpGN',
                            'slug': 'Gooseneck-Trailers',
                            'verbose': 'Gooseneck Trailers'
                        }},
                    ]
                }]
            ]
        cache.set(f'{store.pk}_filters_count_{get_language()}', result, 3600 / 4)
    if count:
        return result, 26 # ToDo: real map + real count
    else:
        return result


def _form_q_filters(query_set):
    result = []
    for category_filter in query_set:
        pre_template = category_filter.field_name
        if category_filter.case_sensitive:
            template = pre_template + '__'
        else:
            template = pre_template + '__i'
        result.append({f'{template}{category_filter.type}': category_filter.filter})
    return result


@register_snippet
class BannerMessage(models.Model):
    text = models.TextField()

    panels = [FieldPanel('text')]

    class Meta:
        verbose_name = "Banner Message"
        verbose_name_plural = "Banner Messages"


class BaseInventory(object):

    def _get_trailers_length(self, trailer_query, last_index):
        digit_pattern = re.compile(r"\d+")
        numerical = lambda x: int(digit_pattern.match(x).group())
        counter = Counter(trailer.length for trailer in trailer_query)
        return [(length, {"index": index, "count": count, "numerical": int(digit_pattern.match(length).group())})
                for index, (length, count) in enumerate(sorted(counter.items(), key=lambda x: numerical(x[0])), last_index)]

    def get_sitemap_urls(self, request=None):
        return []

    def get_trailers_query(self, category, sub_category, store_trailers):
        if sub_category:
            basic_qs = store_trailers.get_trailers_per_subcategory(sub_category)
        elif category:
            basic_qs = store_trailers.get_trailers_per_category(category)
        else:
            basic_qs = store_trailers
        basic_set = sorted(set(basic_qs), key=lambda tr: tr.sale_price)
        return basic_qs, basic_set, store_trailers

    def get_store_trailers(self, request):
        return request.location['store_trailers']

    def serialize_location(self, store, request):
        return serialize_location(store, request)

    def get_types_filters(self, cache_key, queryset, count):
        return _get_types_filter(cache_key, queryset, count)

    @additional_context
    def get_more_context(self, request, store, category, sub_category, *args, **kwargs):
        # Common Context
        context = super().get_context(request, *args, **kwargs)
        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        if request.location["id"] != store.store_id:
            request.location = self.serialize_location(store, request)
        context["store"] = store
        store_trailers = self.get_store_trailers(request)
        basic_qs, basic_set, store_trailers = self.get_trailers_query(category, sub_category, store_trailers)
        context["products"] = dict(
            queryset=[
                {
                    "trailer": trailer,
                    "title": trailer.trailertranslation_set.get(
                        language=get_language().upper()
                    ).tag,
                }
                for trailer in basic_set
            ],
            special=[
                trailer.vin
                for trailer in basic_set
                if (date.today() - trailer.delivery_date).days >= 120
            ],
            count=len(basic_set),
            image_path=path_img('TrailerPictures')
        )
        context["category"] = category
        context["sub_category"] = sub_category
        types, last_index = self.get_types_filters(store, store_trailers, True)
        context["filters"] = {
            "lengths": self._get_trailers_length(basic_qs, last_index),
            "price": basic_qs.aggregate(max=Max('sale_price'), min=Min('sale_price')),
            "types": types,
        }
        context['custom_title'] = build_user_formatted_strings(request, context, self.title)
        context['meta_description'] = build_user_formatted_strings(request, context, self.search_description)
        context['store_slug'] = request.location["slug"]
        context['page_type'] = self.get_verbose_name()
        return context

    def render(self, request, store, category, sub_category, *args, **kwargs):
        request.is_preview = getattr(request, 'is_preview', False)

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            self.get_more_context(request, store, category, sub_category, *args, **kwargs)
        )

def sub_category_size(subcategory):
    if subcategory:
        subcategory = subcategory.upper()
        lenguage = get_language()
        subcategory_dict = {
            'ENC4': {'en':'4\' Cargo', 'es': '4\' Carga'},
            'ENC5': {'en':'5\' Cargo', 'es': '5\' Carga'},
            'ENC6': {'en':'6\' Cargo', 'es': '6\' Carga'},
            'ENC6TA': {'en':'6\' Tandem Cargo', 'es': '6\' Tandem Carga'},
            'ENC7': {'en':'7\' Cargo', 'es': '7\' Carga'},
            'ENC102': {'en':'8.5\' Cargo', 'es': '8.5\' Carga'},
            'FLT4': {'en':'7\' Utility', 'es': '7\' Utilitario'},
            'FLT5': {'en':'5\' Utility', 'es': '5\' Utilitario'},
            'FLT6': {'en':'6\' Utility', 'es': '6\' Utilitario'},
            'FLT6TA': {'en':'6\' Tandem Utility', 'es': '6\' Tandem Utilitario'},
            'FLT7': {'en':'7\' Utility', 'es': '7\' Utilitario'},
            'FLT7TA': {'en':'7\' Tandem Utility', 'es': '7\' Tandem Utilitario'},
            'FLT8': {'en':'8\' Utility', 'es': '8\' Utilitario'},
            'ENCCC': {'en':'Enclosed Car Hauler', 'es': 'Cerrado Porta vehiculos'},
            'FLTCC': {'en':'Flatbed Car Hauler', 'es': 'Plano Porta vehiculos'},
            'ENCATV': {'en':'Enclosed ATV', 'es': 'Cerrado ATV'},
            'FLTATV': {'en':'Flatbed ATV', 'es': 'Plano ATV'},
            'DUMP5': {'en':'5\' Dump', 'es': '5\' Volteo'},
            'DUMP6': {'en':'6\' Dump', 'es': '6\' Volteo'},
            'DUMP7': {'en':'7\' Dump', 'es': '7\' Volteo'},
            'EQP6': {'en':'6\' Equipment', 'es': '6\' Equipo'},
            'EQP7': {'en':'7\' Equipment', 'es': '7\' Equipo'},
            'EQP8': {'en':'8\' Equipment', 'es': '8\' Equipo'},
            'GOOSENECK': {'en':'Gooseneck Trailers', 'es': 'Cuello de cisne'},
        }
        if subcategory in subcategory_dict.keys():
            return subcategory_dict[subcategory][lenguage]

    return ''

class InventoryPage(BaseInventory, Page):
    template = "inventory_base.html"
    cache_prefixes = [
        'cache_product_list_img',
        'cache_social_icons',
        'cache_partners_block',
    ]

    content = StreamField(
        [
            ("product_list", inventory_blocks.ProductList()),
            ("additional_message", inventory_blocks.AdditionalMessage()),
            ("social_icons_banner", common_blocks.SocialIconBanner()),
            ("partners", common_blocks.PartnersBlock()),
        ],
        null=True,
        blank=True,
    )

    seo_block_subcategory = models.TextField(blank=True, null=True)
    seo_block_subcategory_es = models.TextField(blank=True, null=True)
    seo_block_category = models.TextField(blank=True, null=True)
    seo_block_category_es = models.TextField(blank=True, null=True)
    seo_block_inventory = models.TextField(blank=True, null=True)
    seo_block_inventory_es = models.TextField(blank=True, null=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    def select_seo_block(self, category, subcategory, locale):
        lenguage = get_language()
        if subcategory:
            if lenguage == 'en':
                return self.seo_block_subcategory
            else:
                return self.seo_block_subcategory_es
        elif category:
            if lenguage == 'en':
                return self.seo_block_category
            else:
                return self.seo_block_category_es
        else:
            if lenguage == 'en':
                return self.seo_block_inventory
            else:
                return self.seo_block_inventory_es

    @additional_context
    def get_more_context(self, request, store, category, sub_category, *args, **kwargs):
        context = super().get_more_context(request, store, category, sub_category, *args, **kwargs)
        seo_block = self.select_seo_block(category, sub_category, context['locale'])
        context["seo_block"] = seo_block
        context['state'] = context['store'].state
        context['city'] = context['store'].store_city
        context['subcategory_text'] = sub_category_size(sub_category)
        return context


class StatePage(BaseInventory, Page):
    template = "inventory_base.html"
    cache_prefixes = [
        'cache_product_list_img',
        'cache_social_icons',
        'cache_partners_block',
        'cover_banner',
        'h2_title',
        'text_block',
        'store_list',
    ]

    content = StreamField(
        [
            ("product_list", inventory_blocks.ProductList()),
            ("additional_message", inventory_blocks.AdditionalMessage()),
            ("social_icons_banner", common_blocks.SocialIconBanner()),
            ("partners", common_blocks.PartnersBlock()),
            ("cover_banner", common_blocks.CoverBanner()),
            ("centered_title", common_blocks.CenteredTitle()),
            ("store_list", common_blocks.StoreList()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    def beautify(self):
        return ''.join(self.slug).replace('-', ' ')

    @additional_context
    def get_more_context(self, request, *args, **kwargs):
        from trailersplus.utils.objects import list_locations
        category, sub_category = self.get_category_subcategory(request)
        sub = self.get_children().first()
        ms = MyStore.objects.get(slug=sub.slug)
        context = super().get_more_context(request, ms.related_store, category, sub_category, *args, **kwargs)
        context['locations'], context['location_count'] = list_locations(state=self.slug)
        context['slug'] = self.slug
        return context

    def get_category_subcategory(self, request):
        length = len(request.path.split('/'))
        if request.LANGUAGE_CODE not in request.path.split('/'):
            cat = 4
            sub = 5
        else:
            cat = 5
            sub = 6
        category = request.path.split('/')[-2] if length == cat else None
        sub_category = request.path.split('/')[-2] if length == sub else None
        return category, sub_category

    def serve(self, request, *args, **kwargs):
        request.is_preview = getattr(request, 'is_preview', False)

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            self.get_more_context(request, None, None, None, *args, **kwargs)
        )

    def get_store_trailers(self, request):
        return get_store_trailers(None, self.slug)

    def get_sitemap_urls(self, request=None):
        base_url = self.get_full_url(request)
        result = []
        url_parsed = urlparse(base_url)
        lastmod = self.last_published_at or self.latest_revision_created_at
        es_url = url_parsed.scheme + '://' + url_parsed.netloc + '/es' + url_parsed.path
        result.append(
            {
                'location': base_url,
                'lastmod': (lastmod),
            }
        )
        result.append(
            {
                'location': es_url ,
                'lastmod': (lastmod),
            }
        )
        return result

class DetailPage(Page):
    template = "products_base.html"

    cache_prefixes = [
        'cache_product_detail_part1',
        'cache_cta',
        'cache_long_info',
        'cache_partners_block',
        'trustpilot',
        'store_dropdown',
    ]

    content = StreamField(
        [
            ("product_list", detail_page_blocks.ProductPage()),
            ("cta", detail_page_blocks.CTA()),
            ("recently", detail_page_blocks.RecentlyViewed()),
            ("long_info", detail_page_blocks.LongInfo()),
            ("partners", common_blocks.PartnersBlock()),
            ("reserve", detail_page_blocks.Reserve()),
            ("schedule", detail_page_blocks.Schedule()),
            ("appointment", detail_page_blocks.Appointment()),
            ("reviews", detail_page_blocks.Reviews()),
            ("found_lower", detail_page_blocks.FoundLower()),
            ("additional_message", detail_page_blocks.AdditionalMessage()),
            ("trust_pilot_reviews", common_blocks.TrustPilotWidget()),
            ("trust_pilot_reviews_horizontal", common_blocks.TrustPilotWidgetHorizontal()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    @additional_context
    def get_more_context(self, request, store, category, vin, *args, **kwargs):
        context = super(DetailPage, self).get_context(request, *args, **kwargs)
        try:
            trailer = TrailerTranslation.objects.select_related(
                'trailer__category__category_map').prefetch_related('trailer__reviews').get(
                language=get_language().upper(), trailer__vin=vin.upper())
        except TrailerTranslation.DoesNotExist:
            raise Http404("Trailer Does not Exist")
        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        if request.location["id"] != trailer.trailer.store:
            request.location = serialize_location(trailer.trailer.store, request)
        recently_deque = deque(request.session.get('recently_viewed', [None] * 4), maxlen=4)
        context["product"] = {
            "common": trailer.trailer,
            "trans": trailer
        }
        context["store"] = trailer.trailer.store
        context["image_path"] = path_img('Trailers')
        context["reviews"] = {}
        context["reviews"]["data"] = trailer.trailer.reviews.all().order_by('-created_at')[:6]
        context["reviews"]["count"] = trailer.trailer.reviews.all().count()
        context["recently"] = {}
        context["recently"]["special"] = []
        if trailer.trailer.vin not in recently_deque:
            recently_deque.appendleft(vin)
        recent_trailers = TrailerTranslation.objects.select_related('trailer').filter(
            language=get_language().upper(), trailer__vin__in=recently_deque
        ).annotate(delivery_days=Now() - models.F('trailer__delivery_date'))
        context["recently"]["trailers"] = [
            {
                "trailer": x,
                "title": extend_title(
                    x.short_description,
                    x.trailer.vin
                )
            } for x in recent_trailers
        ]
        for recently_vin in recent_trailers:
            if recently_vin.delivery_days.days >= 120:
                context["recently"]["special"].append(recently_vin.trailer.vin)
        context["location"] = {
            "state": request.location["state"],
            "full_state": request.location["full_state"],
            "city": request.location["city"]
        }
        context["category"] = trailer.trailer.category.category_map.slug
        context["images360"] = Image360.objects.filter(vin=trailer.trailer)
        context["extimage360"] = context["images360"].filter(image_type='ext360').exists()
        context["intimage360"] = context["images360"].filter(image_type='int360').exists()
        request.session['recently_viewed'] = list(recently_deque)
        context['custom_title'] = build_user_formatted_strings(request, context, self.title)
        context['meta_description'] = build_user_formatted_strings(request, context, self.search_description)
        context['store_slug'] = request.location["slug"]
        context['detail'] = True
        return context

    # @define_user_location
    def render(self, request, store, category, vin, *args, **kwargs):
        request.is_preview = getattr(request, 'is_preview', False)

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            self.get_more_context(request, store, category, vin, *args, **kwargs)
        )


class CategoryPage(Page):
    template = "category_base.html"

    cache_prefixes =[
        'cache_social_icons',
        'cache_partners_block'
    ]

    content = StreamField(
        [
            ("banner", category_blocks.BannerBlock()),
            ("product_list", category_blocks.ProductsBlock()),
            ("bullets", category_blocks.BulletsBlock()),
            ("social_network", common_blocks.SocialIconBanner()),
            ("partners", common_blocks.PartnersBlock()),
            ("fleet_sales_banner", common_blocks.FleetSalesBanner()),

        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    @additional_context
    def get_more_context(self, request, store, category, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context['store'] = store
        if request.location["id"] != store.store_id:
            request.location = serialize_location(store, request)
        context['store_slug'] = request.location["slug"]
        store_query = request.location["store_trailers"]
        context["categories_count"] = _get_types_filter(store, store_query)
        for index, i_category in enumerate(context['categories_count']):
            if i_category[1]['slug'] == 'Gooseneck':
                context['categories_count'].pop(index)
        basic_query = store_query.filter(category__slug__exact=category)
        context["products"] = dict(
            queryset=[
                {
                    "trailer": trailer,
                    "title": trailer.trailertranslation_set.get(
                        language=get_language().upper()
                    ).short_description,
                }
                for trailer in basic_query
            ],
            special=[
                trailer.vin
                for trailer in basic_query
                if (date.today() - trailer.delivery_date).days >= 120
            ],
            image_path=path_img('Trailers')
        )
        context['custom_title'] = build_user_formatted_strings(request, context, self.title)
        context['meta_description'] = build_user_formatted_strings(request, context, self.search_description)
        context["category_slug"] = category
        context['category'] = category
        return context

    # @define_user_location
    def render(self, request, store, category, *args, **kwargs):
        request.is_preview = getattr(request, 'is_preview', False)

        return TemplateResponse(
            request,
            self.get_template(request, *args, **kwargs),
            self.get_more_context(request, store, category, *args, **kwargs)
        )


def default_related_store():
    try:
        usr = Location.objects.raw("""
            SELECT store_id FROM product_location ORDER BY store_id ASC LIMIT 1;
        """)
        return usr[0].store_id
    except IndexError:
        pass


class MyStore(RoutablePage):
    template = "store_base.html"

    related_inventory = models.SlugField(
        max_length=50,
        null=False,
        blank=True,
        default='inventory'
    )

    related_category = models.SlugField(
        max_length=50,
        null=False,
        blank=True,
        default='category'
    )

    related_detail = models.SlugField(
        max_length=50,
        null=False,
        blank=True,
        default='detail'
    )

    related_store = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='pages',
        default=default_related_store,
    )

    schema_code = models.TextField(blank=True, null=False, default='')

    cache_prefixes = [
        'cache_social_icons',
        'trustpilot',
        'cache_social_icons',
    ]

    content = StreamField(
        [
            ("banner", my_store_blocks.BannerBlock()),
            ("directions", my_store_blocks.DirectionsBlock()),
            ("trust_pilot_reviews", common_blocks.TrustPilotWidget()),
            ("trust_pilot_reviews_horizontal", common_blocks.TrustPilotWidgetHorizontal()),
            ("products", my_store_blocks.ProductsBlock()),
            ("long_text", my_store_blocks.LongTextBlock()),
            ("call_today", my_store_blocks.CallTodayBlock()),
            ("customer_reviews", my_store_blocks.CustomerReviewsBlock()),
            ("one_stop", my_store_blocks.OneStopShopBlock()),
            ("partners", common_blocks.PartnersBlock()),
            ("social", common_blocks.SocialIconBanner()),
            ("get_direction_popup", my_store_blocks.GetDirections()),
            ("appointment_only", detail_page_blocks.Appointment()),
            ("category_carousel", common_blocks.CategoryCarousel()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    settings_panels = Page.settings_panels + [
        MultiFieldPanel(
            [
                FieldPanel('related_inventory'),
                FieldPanel('related_category'),
                FieldPanel('related_detail'),
            ],
            heading="Related SubPages"
        ),
        BaseChooserPanel('related_store', 'Related Store'),
        FieldPanel('schema_code')
    ]

    def get_slug(self):
        return self.get_url()[1:-1]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super(MyStore, self).get_context(request, *args, **kwargs)
        context["headers"] = Header.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["partners"] = Partners.objects.all()
        context["reviews"] = ServiceReviews.objects.all().order_by("-created_at")[:10]
        context["store"] = self.related_store
        context["stores"] = MyStore.objects.all()
        context["message"] = BannerMessage.objects.last().text.format(self.related_store.store_phone)
        trailers = get_store_trailers(self.related_store)
        count = Counter(trailer.category.slug for trailer in trailers)
        result = []
        for category, num in count.items():
            c_t = trailers.filter(category__slug__iexact=category)
            _trailer_pictures = []
            for trailer in c_t[:5]:
                _trailer_picture = trailer.pictures
                if _trailer_picture is None or not len(_trailer_picture) or _trailer_picture[0] is None:
                    _trailer_pictures.append('comingsoon.jpg')
                else:
                    _trailer_pictures.append(_trailer_picture[0]['file'])
            category_ = c_t[0].category
            result.append((category,category_, num, _trailer_pictures, int(c_t.aggregate(Min('sale_price'))['sale_price__min']),
                           c_t[0].category.description))
        context["products"] = sorted(result, key=lambda x: x[3])
        context["products_count"] = len(trailers)
        context["products_image_path"] = path_img('TrailerPictures')

        en_url_path = ['en'] + self.url_path_en.split('/')[2:]
        es_url_path = ['es'] + self.url_path_es.split('/')[2:]
        context["translation_path"] = {
            "en": '/'.join(en_url_path),
            "es": '/'.join(es_url_path),
        }

        return context

    # @define_user_location
    @route(r'^$')
    def render(self, request, *args, **kwargs):
        if request.location["id"] != self.related_store.store_id:
            request.location = serialize_location(self.related_store, request)
        return super(MyStore, self).serve(request, *args, **kwargs)

    @route(r'^inventory/$')
    @route(r'^inventory/(\w+)/$')
    @route(r'^inventory/(\w+)/(\w+)/$')
    @route(r'^inventario/$')
    @route(r'^inventario/(\w+)/$')
    @route(r'^inventario/(\w+)/(\w+)/$')
    def render_inv(self, request, category=None, sub_category=None, *args, **kwargs):
        if category and category.lower() not in (
            'cargo',
            'utility',
            'hauler',
            'atv',
            'dump',
            'equipment',
            'gooseneck'
        ):
            raise Http404
        if sub_category and not Category.objects.filter(web_category__iexact=sub_category).exists():
            raise Http404
        if request.location["id"] != self.related_store.store_id:
            request.location = serialize_location(self.related_store, request)
        inventory_page = InventoryPage.objects.get(slug_en=self.related_inventory)
        return inventory_page.render(request, self.related_store, category, sub_category, *args, **kwargs)

    @route(r'^([0-9a-zA-Z\-]+)/trailer/(\w+)/$')
    def render_detail(self, request, category, vin, *args, **kwargs):
        if not Category.objects.filter(slug__iexact=category).exists():
            raise Http404
        detail_page = DetailPage.objects.get(slug_en=self.related_detail)
        return detail_page.render(request, self.related_store, category, vin, *args, **kwargs)

    def get_sitemap_urls(self, request=None):
        """
        This method only renders urls for basic inventories urls
        all other urls are rendered sith raw sql at sitemaps/inventory.py
        due to performance reasons.
        """
        base_url = self.get_full_url(request)
        result = []
        url_parsed = urlparse(base_url)
        lastmod = self.last_published_at or self.latest_revision_created_at
        es_url = url_parsed.scheme + '://' + url_parsed.netloc + '/es' + url_parsed.path
        result.append(
            {
                'location': base_url + 'inventory/',
                'lastmod': (lastmod),
            }
        )
        result.append(
            {
                'location': es_url + 'inventario/',
                'lastmod': (lastmod),
            }
        )
        return result

    @route(r'^([0-9a-zA-Z\-]+)/$')
    @route(r'^([0-9a-zA-Z\-]+)/$')
    def render_category(self, request, category, *args, **kwargs):
        request.location = serialize_location(self.related_store, request)
        if not Category.objects.filter(slug__iexact=category).exists():
            raise Http404
        store = self.related_store
        category_page = CategoryPage.objects.get(slug_en=self.related_category)
        return category_page.render(request, store, category, *args, **kwargs)
