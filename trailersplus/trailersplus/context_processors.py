from django.utils.translation import get_language
from django.conf import settings

def request_language(request):
    return {'language': get_language()}

def version_number(request):
    return {'version_number': settings.VERSION_NUMBER}