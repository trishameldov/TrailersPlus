from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.base import RedirectView
from django.utils.translation import get_language
from my_store.models import MyStore
from product.models import Location, Trailer, TrailerTranslation
from home.models import Footer, Header, Partners
from menus.models import MainMenu
from flatpage.models import FlatPage

from .models import ErrorPage


def trailer_finder(request):
    if getattr(request, request.method).get('vin'):
        tr = get_object_or_404(Trailer, vin=getattr(request, request.method).get('vin'))
        ms = get_object_or_404(MyStore, related_store=tr.store)
        url = f'{ms.url}{tr.category.slug}/trailer/{tr.vin}/'
        return redirect(url)
    return render(request, 'home/trailer-finder.html')


def trailer_finder_appt(request):
    if hasattr(request, request.method):
        if getattr(request, request.method).get('vin'):
            tr = get_object_or_404(Trailer, vin=getattr(request, request.method).get('vin'))
            ms = get_object_or_404(MyStore, related_store=tr.store)
            url = f'{ms.url}{tr.category.slug}/trailer/{tr.vin}/#schedule'
            return redirect(url)
    return render(request, 'home/trailer-finder.html')


def error_404_view(request: HttpRequest, exception):
    try:
        error_page = ErrorPage.objects.get(slug_en__iexact="404")
        template_response = error_page.serve(request)
        content_rendered = template_response.render()
    except ErrorPage.DoesNotExist:
        return HttpResponseNotFound("Please create page with slug \"404\"")
    else:
        return HttpResponseNotFound(content_rendered)


def search_redirect(request):
    url = f'{request.scheme}://{request.site_name}/'
    tt = request.GET.get('trailer-type', 'all')
    try:
        ts = Location.objects.get(
            store_city=request.GET.get('trailer-store', None)
        ).get_slug()
    except Location.DoesNotExist:
        return redirect(url)
    url += f'{ts}/inventory/'
    if tt != 'all':
        url += tt
    return redirect(url)


def thankyou_page(request):
    if request.method == 'POST':
        language = get_language()
        try:
            translation = TrailerTranslation.objects.get(trailer__vin=request.POST['trailer_vin'], language=language.upper())
        except TrailerTranslation.DoesNotExist:
            translation = None
        
        context = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'appointmen_date': request.POST.get('date'),
            'language': language,
        }

        if translation is not None:
            context["trailer_title"] = translation.short_description
            context["trailer"] = translation.trailer
            context["translation"] = translation
        
        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["location_count"] = 0
        
        return render(request, 'home/thankyou.html', context)

    else:
        page = get_object_or_404(FlatPage, slug='thankyou')
        return page.serve(request)

def thankyou_page_service(request):
    if request.method == 'POST':
        language = get_language()
        translation = None
        
        context = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'store_name': request.POST.get('store_name'),
            'store_address': request.POST.get('store_address'),
            'store_location': request.POST.get('store_location'),
            'appointmen_date': request.POST.get('date'),
            'language': language,
        }

        if translation is not None:
            context["translation"] = translation
        
        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["location_count"] = 0
        
        return render(request, 'home/thankyou_service.html', context)

    else:
        page = get_object_or_404(FlatPage, slug='thankyou')
        return page.serve(request)

    


def robots_txt(request):
    staging_disallow = "\nDisallow: /" if settings.DEBUG else ""
    return HttpResponse(
        "Sitemap: https://www.trailersplus.com/sitemap.xml\n\n"
        "User-Agent: *\n"
        "Disallow: /invoice/\n"
        "Disallow: /thankyou/\n"
        "Disallow: /trailer-finder/\n"
        "Disallow: /checkout/\n"
        f"Disallow: /404/{staging_disallow}",
        content_type="text/plain", status=200)


class BlogRedirectView(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        path = kwargs['slug']
        url = f'{self.request.scheme}://{settings.SITE_NAME}/{path}'
        return url
