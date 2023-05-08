from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2

def ip_country(request, customer_ip):
    g = GeoIP2()
    location_info = g.country(customer_ip)
    if location_info["country_code"] == "US" or settings.DEBUG:
        validation =  True
    else:
        raise ValueError
    return validation
