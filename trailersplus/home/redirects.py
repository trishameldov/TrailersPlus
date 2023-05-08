from django import http

from wagtail.contrib.redirects import models
from wagtail.contrib.redirects.middleware import get_redirect
from wagtail.core.models import Site

def check_for_redirects(request):
    # No need to check for a redirect for non-404 responses.
    # Get the path
    path = models.Redirect.normalise_path(request.get_full_path())
    # Find redirect
    redirect = get_redirect(request, path)
    if redirect is None or redirect.link is None:
        redirect = check_wild_card_redirects(request, path)
    if redirect is not None:
        return route_redirect(redirect)
    return None

def check_wild_card_redirects(request, path):
    site = Site.find_for_request(request)
    wildcards = models.Redirect.get_for_site(site).filter(old_path__contains='*')
    for wildcard in wildcards:
        if  wildcard.old_path.count('*') == 1:
            # wildcard.old_path = '/California/Santa_Rosa/*'
            # partial_old_path = '/California/Santa_Rosa/'
            # wildcard.link = 'http://127.0.0.1:8000/California/Petaluma/*'
            # partial_link = 'http://127.0.0.1:8000/California/Petaluma/'
            # path = '/California/Santa_Rosa/5-Wide-Utility-Trailers/trailer/4YMBU0811MN032035/'
            # path = path.replace(partial_old_path, partial_link)
            # >> '/California/Petaluma/5-Wide-Utility-Trailers/trailer/4YMBU0811MN032035/'
            condition = path.startswith(wildcard.old_path.split('*')[0])
        else:
            # wildcard.old_path = '/*/Santa_Rosa/*'
            # partial_old_path = '/Santa_Rosa/'
            # wildcard.link = 'http://127.0.0.1:8000/*/Petaluma/*'
            # partial_link = '/Petaluma/'
            # path = '/California/Santa_Rosa/5-Wide-Utility-Trailers/trailer/4YMBU0811MN032035/'
            # path = path.replace(partial_old_path, partial_link)
            # >> '/California/Petaluma/5-Wide-Utility-Trailers/trailer/4YMBU0811MN032035/'
            condition = wildcard.old_path.split('*')[wildcard.link.count('*') -1] in path
        if condition:
            acceptable_counts = [1, 2]
            if (
                wildcard.link.count('*') in acceptable_counts and
                wildcard.old_path.count('*') in acceptable_counts and
                wildcard.old_path.count('*') == wildcard.link.count('*')
            ):
                partial_old_path = wildcard.old_path.split('*')[wildcard.link.count('*') -1]
                partial_link = wildcard.link.split('*')[wildcard.link.count('*') -1]
                path = path.replace(partial_old_path, partial_link)
                return path
    return None

def route_redirect(redirect):
    if isinstance(redirect, str) or redirect.is_permanent:
        try:
            return http.HttpResponsePermanentRedirect(redirect.link)
        except AttributeError:
            return http.HttpResponsePermanentRedirect(redirect)
    return http.HttpResponseRedirect(redirect.link)