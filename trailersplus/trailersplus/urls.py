from checkout import views
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path
from home.views import (BlogRedirectView, robots_txt, search_redirect,
                        thankyou_page, trailer_finder, trailer_finder_appt, thankyou_page_service)
from search import views as search_views
from sitemaps.inventory import sitemaps
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls

from . import wagtailurls

urlpatterns = [
    path("thankyou/", thankyou_page, name="thankyou_page"),
    path("thankyou-for-your-service-appointment/", thankyou_page_service, name="thankyou_page_service"),
    url(r"^django-admin/", admin.site.urls),
    url(r"^admin/", include(wagtailadmin_urls)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt', robots_txt, name="robotstxt_file"),
    url(r"^documents/", include(wagtaildocs_urls)),
    url(r"^i18n/", include("django.conf.urls.i18n")),
    url(r"^search/$", search_views.search, name="search"),
    url(r"^api/", include("api.urls")),
    url(r"^en/api/", include("api.urls")),
    url(r"^es/api/", include("api.urls")),
    url(r"^submit/$", search_redirect, name="Search Trailers Form Redirect"),
    url(r"^en/submit/$", search_redirect, name="Search Trailers Form Redirect"),
    url(r"^es/submit/$", search_redirect, name="Search Trailers Form Redirect"),
    url(r"^checkout-submit/$", views.submit, name="Checkout submit"),
    url(r"^en/checkout-submit/$", views.submit, name="Checkout submit"),
    url(r"^es/checkout-submit/$", views.submit, name="Checkout submit"),
    path('checkout/<str:trailer_id>/', views.redirect_checkout_vin, name='redirect_checkout_vin'),
    url(r"^trailer-finder/$", trailer_finder, name="trailer-finder"),
    url(r"^en/trailer-finder/$", trailer_finder, name="trailer-finder_en"),
    url(r"^es/trailer-finder/$", trailer_finder, name="trailer-finder_es"),
    url(r"^trailer-finder-appt/$", trailer_finder_appt, name="trailer_finder_appt"),
    url(r"^en/trailer-finder-appt/$", trailer_finder_appt, name="trailer_finder_appt_en"),
    url(r"^es/trailer-finder-appt/$", trailer_finder_appt, name="trailer_finder_appt_es"),
    path("invoice/<str:invoice_id>/", views.InvoiceView.as_view(), name="invoice"),
    path("invoice/ach", views.invoice_payment_ach, name="invoice_ach"),
    path("en/blog/<str:slug>/", BlogRedirectView.as_view(), name="blogredirecten"),
    path("es/blog/<str:slug>/", BlogRedirectView.as_view(), name="blogredirectes"),
]

# Multilang patterns
urlpatterns += i18n_patterns(url(r"", include(wagtailurls)),)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    # Serve static and media files from development server

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtailurls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r"^pages/", include(wagtail_urls)),
]

handler404 = 'home.views.error_404_view'
