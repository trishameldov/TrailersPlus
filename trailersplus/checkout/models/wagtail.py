import re
import datetime as dt

from django.conf import settings

from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from streams import blocks
from streams.splitted_blocks.commerce_blocks import detail_page_blocks as d_blocks
from checkout.services import WebsiteApiClient
from trailersplus.utils.decorators import define_user_location, additional_context
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from trailersplus.celery import app
from product.models.django import Trailer
from django.utils.translation import get_language
from trailersplus.utils.celery import wait_for_result
from .django import TestInvoice


class RedirectNeeded(Exception):
    """raised to be proceed and call redirect"""
    pass


class CheckoutPage(Page):
    template = "checkout_base.html"

    content = StreamField(
        [
            ('checkout', blocks.CheckoutBlock()),
            ('long_text', d_blocks.LongInfo()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        from home.models import Footer, Header
        from menus.models import MainMenu
        # FixMe: Fix this import
        # If import home.models on top the Circular import error raises
        context["headers"] = Header.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()

        # There are four ways to enter this page and provide the trailer's VIN:
        #     - Via the 'Reserve' button in the product page.
        #     - Via the 'checkout' button in the cart.
        #     - Via entering the url '/checkout/<vin>'
        #     - Via entering the url '/checkout/' and adding the vin as a
        #           query parameter.

        # Grabs the vin from the query params.
        # The url '/checkout/<vin>' directs to a view that redirects to this page
        # and adds the vin as a query param.
        trailer_id = request.GET.get('vin')

        # If there is none, grabs the trailer that is in the cart.
        if not trailer_id:
            try:
                cart_pattern = re.compile(r'[0-9A-Za-z]{10,21}')
                trailer_id = cart_pattern.search(request.session.get('cart_item', '')).group()
            except (KeyError, ValueError, TypeError, AttributeError):
                try:
                    raise RedirectNeeded(request.META['HTTP_REFERER'])
                except KeyError:
                    raise RedirectNeeded(f'{request.scheme}://{request.site_name}/')

        trailer = Trailer.objects.get(vin=trailer_id)
        context["cart_trailer"] = {
            'info': trailer,
            'title': trailer.trailertranslation_set.get(language=get_language().upper()).short_description,
            'image_path': '/web-pictures/Trailers',
            'store': trailer.store

        }
        en_url_path = ['en'] + self.url_path_en.split('/')[2:]
        es_url_path = ['es'] + self.url_path_es.split('/')[2:]
        context["translation_path"] = {
            "en": '/'.join(en_url_path),
            "es": '/'.join(es_url_path),
        }
        context["AUTHORIZE_CLIENT_KEY"] = settings.AUTHORIZE_CLIENT_KEY
        context["AUTHORIZE_LOGIN_ID"] = settings.AUTHORIZE_LOGIN_ID
        context["AUTHORIZE_JS_URL"] = settings.AUTHORIZE_JS_URL

        return context

    # @define_user_location
    def serve(self, request, *args, **kwargs):
        try:
            response = super().serve(request, *args, **kwargs)
            response['Cache-Control'] = 'no-cache, max-age=0'
            response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'

            return response
        except RedirectNeeded as rd:
            return redirect(str(rd))


    def get_sitemap_urls(self, request=None):
        return []


class CheckoutTnxPage(Page):
    template = "checkout_base.html"

    content = StreamField(
        [
            ('main_content', blocks.CheckoutTnxBlock()),
            ("social_icons_banner", blocks.SocialIconBanner()),
            ('partners', blocks.PartnersBlock()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        from home.models import Footer, Header, Partners
        from menus.models import MainMenu
        # FixMe: Fix this import
        # If import home.models on top the Circular import error raises
        context["headers"] = Header.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["partners"] = Partners.objects.all()
        try:
            invoice_id = str(request.session['last_invoice'])
        except KeyError:
            invoice_id = request.GET.get('invoice_id', '')
            if '-' in invoice_id:
                invoice_id = invoice_id.split('-')
                store_id = invoice_id[0]
                invoice_id = invoice_id[1]
        print(f"Success: {invoice_id=}")
        if not invoice_id:
            if not settings.DEBUG:
                try:
                    raise RedirectNeeded(request.META['HTTP_REFERER'])
                except KeyError:
                    raise RedirectNeeded(f'{request.scheme}://{request.site_name}/')
            else:
                invoice_id = settings.DEFAULT_INVOICE
        object = WebsiteApiClient()
        try:
            invoice = TestInvoice.objects.get(invoice_id=invoice_id)
        except TestInvoice.MultipleObjectsReturned:
            invoice = TestInvoice.objects.filter(invoice_id=invoice_id).last()
        except TestInvoice.DoesNotExist as e:
            if settings.DEBUG:
                invoice = TestInvoice.objects.first()
            if not request.GET.get('invoice', None):
                invoice = object.create_in_db(request.GET.get('invoice_uuid'))
        trailer = invoice.trailer
        context["cart_trailer"] = {
            'info': trailer,
            'title': trailer.trailertranslation_set.get(language=get_language().upper()).short_description,
            'image_path': '/web-pictures/Trailers',
            'store': trailer.store
        }
        context["store"] = trailer.store
        context["invoice"] = invoice
        context["invoice_id"] = request.GET.get('invoice_id', None)
        context["invoice_uid"] = request.GET.get('invoice_uuid', None)

        en_url_path = ['en'] + self.url_path_en.split('/')[2:]
        es_url_path = ['es'] + self.url_path_es.split('/')[2:]
        context["translation_path"] = {
            "en": '/'.join(en_url_path),
            "es": '/'.join(es_url_path),
        }

        return context

    def get_sitemap_urls(self, request=None):
        return []

    # @define_user_location
    def serve(self, request, *args, **kwargs):
        try:
            response = super().serve(request, *args, **kwargs)
            response['Cache-Control'] = 'no-cache, max-age=0'
            response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'

            return response
        except RedirectNeeded as rd:
            return redirect(str(rd))
