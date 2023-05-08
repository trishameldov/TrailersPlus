from django.conf import settings
from django.http.response import Http404
from django.shortcuts import redirect
from django.utils.cache import patch_cache_control
from my_store.models import MyStore, StatePage
from wagtail.core import views
from wagtail.core.models import Page, Site
from wagtail.core.url_routing import RouteResult

from .redirects import check_for_redirects
#
# REFERENCES
#    - https://github.com/wagtail/wagtail/issues/794
#


def pageroute_iexact(page, request, path_components, language):
    if path_components:
        # request is for a child of this page
        child_slug = path_components[0]
        remaining_components = path_components[1:]
        try:
            subpage = page.get_children().get(slug_en__iexact=child_slug, slug_es__iexact=child_slug)
            language = request.LANGUAGE_CODE.lower()
        except Page.DoesNotExist:
            try:
                subpage = page.get_children().get(slug_en__iexact=child_slug)
                language = "en"
            except Page.DoesNotExist:
                try:
                    subpage = page.get_children().get(slug_es__iexact=child_slug)
                    language = "es"
                except Page.DoesNotExist:
                    if isinstance(page, MyStore):
                        return  language, page.route(request, path_components)
                    elif isinstance(page, StatePage):
                        return pageroute_iexact(page.specific, request, remaining_components, language)
                    else:
                        raise Http404
        return pageroute_iexact(subpage.specific, request, remaining_components, language)
    else:
        # request is for this very page
        if page.live:
            return language, RouteResult(page)
        else:
            raise Http404


original_serve = views.serve


def wagtail_serve_monkey_patch_view(request, path):
    if request.LANGUAGE_CODE.lower() == 'es':
        language = f'/{request.LANGUAGE_CODE}'
    else:
        language = ''
    try:
        request.canonical_url = f'{request.scheme}://{settings.SITE_NAME}{language}/{path}'
        response = original_serve(request, path)
    except Http404:
        response = check_for_redirects(request)
        if response:
            return response
        # we need a valid Site object corresponding to this request to proceed
        site = Site.find_for_request(request)
        if site:
            path_components = [component for component in path.split('/') if component]
            try:
                lang, route_result = pageroute_iexact(site.root_page.specific, request, path_components, language)
            except Http404:
                pass
            else:
                if isinstance(route_result.page, MyStore):
                    try:
                        name = route_result[1][0]._routablepage_routes[0][0].name
                    except IndexError:
                        url = route_result.page.url
                    else:
                        ar = route_result[1][1]
                        page_instance = route_result.page
                        relative_path = page_instance.reverse_subpage(name, args=ar)
                        url = page_instance.url + relative_path
                else:
                    url = getattr(route_result.page, f'url_path_{lang}').replace('/home', '')
                if lang != request.LANGUAGE_CODE.lower():
                    response = redirect(url)
                    response.set_cookie(
                        settings.LANGUAGE_COOKIE_NAME, lang,
                        max_age=settings.LANGUAGE_COOKIE_AGE,
                        path=settings.LANGUAGE_COOKIE_PATH,
                        secure=settings.LANGUAGE_COOKIE_SECURE,
                        httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                        samesite=settings.LANGUAGE_COOKIE_SAMESITE,
                    )
                    return response
                try:
                    request.canonical_url = f'{request.scheme}://{site.hostname}{url}'
                    response = original_serve(request, url)
                except Http404:
                    try:
                        request.canonical_url = f'{request.scheme}://{site.hostname}{url}'
                        url = "/"+"/".join(url.split('/')[2:])
                        response = original_serve(request, url)
                    except Http404:
                        raise
                patch_cache_control(response, max_age=3600)

        # If we cannot route to a suitable page, re-raise the original 404.
        if not response:
            raise
    
    return response


views.serve = wagtail_serve_monkey_patch_view

