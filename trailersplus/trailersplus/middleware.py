import math
import re
import socket
from typing import Dict

import geoip2.errors
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from my_store.models import serialize_location
from product.models import Location
from api.utils import get_ip_customer


class UserLocationMiddleware(MiddlewareMixin):
    """Checks if the user's closest store is stored in the session and if not, determines it"""

    # Earth Radius
    R = 6378.1

    def process_request(self, request: HttpRequest):
        location = request.session.get('user_location', None)
        if location is None or not re.match(r'\w{4}\d{2}', str(location)):
            location = self._define_closest_store(request)
            request.session['user_location'] = location.store_id
            request.session.modified = True
        else:
            try:
                location = Location.objects.get(store_id=location,active=True)
            except Location.DoesNotExist:
                location = self._define_closest_store(request)
        request.location = serialize_location(location, request)

    def _define_closest_store(self, request: HttpRequest) -> Location:
        g = GeoIP2()
        ip = get_ip_customer(request)
        if self._ip_is_valid(ip):
            location_info = g.city(ip)
            state_stores_query = Location.objects.filter(state=location_info['region'],active=True)
            if state_stores_query.exists():
                return self._get_closest(location_info, state_stores_query)
            elif len(location_info) == 1:
                return state_stores_query[0]
            else:
                return self._get_closest(location_info, Location.objects.filter(active=True))
        else:
            return Location.objects.first()

    def _get_distance(self, lat1: str, lon1: str, lat2: str, lon2: str) -> float:
        lon1 = math.radians(float(lon1))
        lon2 = math.radians(float(lon2))
        lat1 = math.radians(float(lat1))
        lat2 = math.radians(float(lat2))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return self.R * c

    def _get_closest(self, location_info: Dict, locations_query: Location.objects) -> Location:
        closest = None
        lat1 = location_info['latitude']
        lon1 = location_info['longitude']
        for location in locations_query:
            distance = self._get_distance(lat1,
                                          lon1,
                                          location.store_lat,
                                          location.store_long)
            if closest is None or \
                    closest[1] > distance:
                closest = location, distance
        return closest[0]

    @staticmethod
    def _ip_is_valid(ip: str) -> bool:
        try:
            if not ":" in ip:
                socket.inet_aton(ip)
            GeoIP2().coords(ip)
            return True
        except (socket.error, geoip2.errors.AddressNotFoundError):
            return False


class LocationTagMiddleware(MiddlewareMixin):

    def process_response(self, request: HttpRequest, response: HttpResponse):
        if 'admin' not in request.path:
            location_pattern = re.compile(b'(&lt;|<)\s?location_slug\s?(&gt;|>)')
            rc = response.content
            rc = location_pattern.sub(str.encode(request.location['slug']), rc)
            response.content = rc
            if "Content-Length" in response:
                response["Content-Length"] = len(response.content)
        return response


class RequestSiteName(MiddlewareMixin):

    def process_request(self, request: HttpRequest):
        request.site_name = settings.SITE_NAME


class CacheRemovalMiddleware(MiddlewareMixin):
    """Removes Cache from Staging responses."""

    def process_response(self, request: HttpRequest, response: HttpResponse):
        if settings.DEBUG:
            response['Cache-Control'] = 'no-cache, max-age=0'
            response['Expires'] = 'Fri, 01 Jan 1990 00:00:00 GMT'
        return response