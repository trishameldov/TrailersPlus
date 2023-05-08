import re
from datetime import datetime
from importlib.resources import path

import pytz
from django.conf import settings
from django.utils import timezone
from product.models import Trailer


def titeliser(text):
    pattern = re.compile(r"([\w ]+)[.,;:-]")
    match = re.findall(pattern, text)
    try:
        return match[0][:120]
    except IndexError:
        return text[:120]


def get_date(text):
    try:
        regex = r"(?P<day>\d{2})-(?P<month>\d{2})-(?P<year>\d{4})T(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}).+"
        pattern = re.compile(regex)
        time = pattern.match(text)
        if time is None:
            raise ValueError
        else:
            time_dict = {key: int(value) for key, value in time.groupdict().items()}
            return datetime(**time_dict, tzinfo=pytz.UTC)
    except ValueError:
        regex = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T(?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}).+"
        pattern = re.compile(regex)
        time = pattern.match(text)
        if time is None:
            return timezone.now()
        else:
            time_dict = {key: int(value) for key, value in time.groupdict().items()}
            return datetime(**time_dict, tzinfo=pytz.UTC)


def get_trailer(mpn):
    if not len(trailers := Trailer.objects.filter(category__base_type=mpn)):
        return
    else:
        return trailers


def path_img(prefix):
    suffix = f'/web-pictures/{prefix}'
    if not settings.DEBUG:
        ds800 = '/cdn-cgi/image/width=800,quality=75,format=webp' + suffix
        ds600 = '/cdn-cgi/image/width=600,quality=75,format=webp' + suffix
        ds400 = '/cdn-cgi/image/width=400,quality=75,format=webp' + suffix
        ds300 = '/cdn-cgi/image/width=300,quality=75,format=webp' + suffix
        ds200 = '/cdn-cgi/image/width=200,quality=75,format=webp' + suffix
        dsCart = '/cdn-cgi/image/width=200,quality=75,format=webp' + prefix
        original = '/cdn-cgi/image/quality=75,format=webp' + suffix
        return {'original':original ,'ds200': ds200,'ds300': ds300,'ds400': ds400,'ds800': ds800,'ds600': ds600, 'dsCart': dsCart}
    return {'original':suffix ,'ds200': suffix,'ds300': suffix,'ds400': suffix,'ds800': suffix,'ds600': suffix, 'dsCart': prefix}

def get_ip_customer(request):
    try:
        customer_ip = request.headers['X-Forwarded-For'].split(',')[0]
    except (KeyError, IndexError):
        try:
            customer_ip = request.headers['X-Real-Ip'].split(',')[0]
        except KeyError as e:
            if settings.DEBUG:
                return '127.0.0.1'
            raise e
    return customer_ip
