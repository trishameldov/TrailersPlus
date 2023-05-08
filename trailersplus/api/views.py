import time
import datetime as dt
import logging

from authorizenet import apicontractsv1
from authorizenet.constants import constants
from authorizenet.apicontrollers import createTransactionController
from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Value
from django.db.models import F
from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework import viewsets
from django.db import transaction, models

from checkout.models import TestInvoice
from checkout.utils import ip_country
from .serializers import LocationSerializer
from product.models import Location, Trailer, Service
from django.utils.translation import get_language
from .permissions import IsAdminUserOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, CSRFCheck
from rest_framework.pagination import PageNumberPagination, replace_query_param
from rest_framework.views import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .models import ProductReviews
from math import ceil
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.backends.db import SessionStore
from checkout.services import WebsiteApiClient, authorizenet_process
from django.core.exceptions import ObjectDoesNotExist
from geopy.geocoders import Nominatim

from .models import (
    LowerPrice,
    Appointment,
    Custom,
    Fleet,
    Warranty,
    WarrantyPhoto,
)

from .serializers import (
    LowerPriceSerializer,
    AppointmentSerializer,
    CustomSerializer,
    FleetSerializer,
    WarrantySerializer,
    WarrantyPhotoSerializer,
    VINTrailerSerializer,
    ProductReviewsSerializer,
    ReserveSerializer,
)

import json
from .tasks import save_review
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import HttpResponse, get_object_or_404
from my_store.models import get_store_trailers
from api.utils import get_ip_customer

from trailersplus.utils.objects import list_locations


logger = logging.getLogger(__name__)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.filter(active=True)
    serializer_class = LocationSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def list(self, *args, **kwargs):
        if get_language() == 'es':
            titles = {
                "get_direction_title": "Obtener las Direcciones",
                "view_store_invent_title": "Ver Inventario de la Tienda",
                "set_store_title": "Establecer Como mi Tienda",
                "more_information_title": "Más información",
                "store_hours_title": "Horarios",
            }
        else:
            titles = {
                "get_direction_title": "Get Directions",
                "view_store_invent_title": "View Store Inventory",
                "set_store_title": "Set Store as Default",
                "more_information_title": "More Information",
                "store_hours_title": "Store Hours",
            }
        response = {
            "locations": sorted(self.serializer_class(
                self.get_queryset(), many=True, context=self.get_serializer_context()
            ).data, key=lambda x: x['store_city']),
            "titles": titles,
        }
        return Response(response)

    def get_serializer_context(self):
        locale = get_language()
        context = super(LocationViewSet, self).get_serializer_context()
        context.update({"locale": locale, "request": self.request})
        return context


class ProductReviewsPagination(PageNumberPagination):
    page_size = 6
    max_page_size = 6

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        page_number = ceil(self.page.paginator.count / self.page_size)
        return replace_query_param(url, self.page_query_param, page_number)

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        page_number = 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'first': self.get_first_link(),
                'last': self.get_last_link(),
            },
            'count': self.page.paginator.count,
            'last_page_number': ceil(self.page.paginator.count / self.page_size),
            'results': data
        })


class ProductReviewsList(ListAPIView):
    serializer_class = ProductReviewsSerializer
    permission_classes = [AllowAny]
    pagination_class = ProductReviewsPagination

    # def list(self, request, trailer_vin, *args, **kwargs):
    #     queryset = Trailer.objects.prefetch_related('reviews').get(vin=trailer_vin).reviews.all()
    #     result_page = self.pagination_class.paginate_queryset(queryset, request)
    #     serializer = ProductReviewsSerializer(result_page, many=True)
    #     return self.pagination_class.get_paginated_response(serializer.data)

    def get_queryset(self):
        trailers = Trailer.objects.get(vin=self.request.query_params['vin'])
        reviews = ProductReviews.objects.filter(products=trailers)[6:]
        return reviews


class LowerPriceCreate(CreateAPIView):
    queryset = LowerPrice.objects.all()
    serializer_class = LowerPriceSerializer
    permission_classes = [AllowAny]


class AppointmentCreate(CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [AllowAny]


def get_available_appointment(request,store, date):
    redis_client = WebsiteApiClient()
    return JsonResponse(redis_client.available_appointment_slots(store, f"{date} 0:00:00", f"{date} 20:00:00"), safe=False)
    # Método temporal para regresar json
    # return JsonResponse(
    #     # Esto regresa la consola en staging
    #     [{
    #         "start":1660231800,
    #         "display_string":"3:30 PM - 4:30 PM",
    #         "end":1660235400,
    #         "store_id":"TRPL09",
    #         "appointment_id":756295
    #     },
    #     {
    #         "start":1660228200,
    #         "display_string":"2:30 PM - 3:30 PM",
    #         "end":1660231800,
    #         "store_id":"TRPL09",
    #         "appointment_id":756297
    #     }], safe=False
    # )

def get_available_service_appointment(request, store, date):
    redis_client = WebsiteApiClient()
    date_user = dt.datetime.strptime(date, '%Y-%m-%d')
    redis_response = redis_client.available_service_appointment_slots(store, f"{date} 0:00:00", f"{date} 20:00:00")

    response = []

    if redis_response:
        response = []
        for appt in redis_response:
            date_appt = dt.datetime.fromtimestamp(appt['start'])
            if date_appt.date() == date_user.date():
                response.append(appt)


    return JsonResponse(response, safe=False)
    
    
    # Example return JSON:
    # return JsonResponse(
    #     [{
    #         'appointment_id': 688091,
    #         'display_string':'10:00 PM - 11:00 PM',
    #         'end': 1660231800,
    #         'start': 1660228200,
    #         'store_id': u'TRPL09'
    #     },
    #     {
    #         'appointment_id': 688092,
    #         'display_string':'12:00 PM - 13:30 PM',
    #         'end': 1660231800,
    #         'start': 1660228200,
    #         'store_id': u'TRPL09'
    #     },
    #     {
    #         'appointment_id': 688093,
    #         'display_string':'2:30 PM - 3:30 PM',
    #         'end': 1660231800,
    #         'start': 1660228200,
    #         'store_id': u'TRPL09'
    #     }], safe=False)
    


def get_store_services(request, store_id):
    """Return a JSON with all services for a given store."""

    try:
        store = Location.objects.get(store_id__iexact=store_id)
    except Location.DoesNotExist:
        response = [{"error": True, "message": "No location found", "description": None}]
    
    if get_language() == 'en':
        services = Service.objects.filter(location=store).order_by('name')
    else:
        services = Service.objects.filter(location=store).order_by('name_es')

    if services.exists():
        if get_language() == 'en':
            response = [{"name": service.name, "description": service.description} for service in services]
        else:
            response = [{"name": service.name_es, "description": service.description_es} for service in services]

    else:
        if get_language() == 'en':
            response = [{"error": True, "message": "No services available", "description": None}]
        else:
            response = [{"error": True, "message": "No hay servicios disponibles", "description": None}]
        # Example response
        # response = [{"name": "2 Part D-Rings", "description": None}, {"name": "Aero-Flow Vent Installation", "description": None}, {"name": "Brake Adjustment", "description": None}, {"name": "Brake Controller Install (Plug and Play)", "description": None}, {"name": "Carry-On / Patriot Dump tarp install", "description": None}, {"name": "Door Catch Installation", "description": None}, {"name": "Door Handle Installation", "description": None}, {"name": "E-Track Installation (Floor Mount)", "description": None}, {"name": "Fender Install", "description": None}, {"name": "Fix Common Wiring Issues", "description": None}, {"name": "Ramp Transition Flap Install", "description": None}, {"name": "Rubber Bumper", "description": None}, {"name": "Surface Mount Tie Down Install", "description": None}, {"name": "Tire Mount - Bolt On", "description": None}, {"name": "Tire Swap", "description": None}, {"name": "Top Wind Jack Install", "description": None}, {"name": "12V Battery Installation", "description": None}, {"name": "Anti-Sway Hitch/Weight Distribution", "description": None}, {"name": "BK-100 Wheel Chock Install", "description": None}, {"name": "BK-103 Wheel Chock Install", "description": None}, {"name": "BK-200 Ratchet Strap Install", "description": None}, {"name": "Cam Bar Upgrade", "description": None}, {"name": "E-Track Installation (Wall Mount)", "description": None}, {"name": "H/D D-Rings Install", "description": None}, {"name": "Leaf Spring Replacement", "description": None}, {"name": "Spring Assist Adjustment", "description": None}, {"name": "Bearing Replacement", "description": None}, {"name": "Brake Upgrade (Single Axle)", "description": None}, {"name": "Dome Light Installation", "description": None}, {"name": "Dump Trailer Side Extension Install - Bolt On", "description": None}, {"name": "Floor Repair", "description": None}, {"name": "Ladder Rack Install (Side Mount)", "description": None}, {"name": "Load Light Install", "description": None}, {"name": "Rear Stabilizer Jack Install - Bolt On", "description": None}, {"name": "Recessed Ratchet Tie Downs", "description": None}, {"name": "Recessed Wheel Chock Install", "description": None}, {"name": "RV Door R&R", "description": None}, {"name": "Solar Panel Install", "description": None}, {"name": "Spring Axle Replacement", "description": None}, {"name": "Stone Guard R&R", "description": None}, {"name": "Tire Mount - Weld On", "description": None}, {"name": "Tongue Box Install", "description": None}, {"name": "Awning / Concession Doors", "description": None}, {"name": "Coupler Replacement", "description": None}, {"name": "Custom Fabrication Racks", "description": None}, {"name": "Dump Trailer Side Extension Install - Weld On", "description": None}, {"name": "Flush Lock Cam Door Install", "description": None}, {"name": "Fuel Door Install", "description": None}, {"name": "Ladder Rack Install (One Piece Roof)", "description": None}, {"name": "Ladder Rack Install (Roof Wrap/D-92 Ladder Rack)", "description": None}, {"name": "Rear Stabilizer Jack Install - Weld On", "description": None}, {"name": "Roof Cap R&R", "description": None}, {"name": "Roof Wrap Replacement", "description": None}, {"name": "Skin Sheet Replacement", "description": None}, {"name": "Structural R&R damage", "description": None}, {"name": "Winch Install", "description": None}, {"name": "Window Install Horizontal", "description": None}]


    return JsonResponse(response, safe=False)


def point_from_zipcode(zipcode):
    geolocator = Nominatim(user_agent="api")
    location = geolocator.geocode(
        query={
            "postalcode": zipcode,
            "country": "US",
        },
        addressdetails=True,
    )
    coordinates = (location.longitude, location.latitude)
    return Point(coordinates, srid=4326)


@csrf_exempt
def get_zip_stores(request, zip_code):
    """Returns the three closest locations to a given ZipCode."""

    try:
        user_pnt = GEOSGeometry(point_from_zipcode(zip_code))
    except AttributeError:
        error_msg = {'error': True, 'message': 'Error ocurred, select a store from the dropdown'}
        return JsonResponse(error_msg, safe=False, status=500)

    queryset = Location.objects.annotate(distance=Distance('point', user_pnt)).order_by('distance')[:3]

    response = []
    for query in queryset:

        distance = round(query.distance.mi, 2)

        response.append(
            {
                "store_name": query.store_name,
                "state": query.state,
                "store_address": query.store_address,
                "city": query.store_city,
                "store_zip": query.store_zip,
                "distance": f"{distance} miles",
                "id": query.store_id,
            }
        )

    return JsonResponse(response, safe=False)


def get_customer_appointments(request, customer_id):
    redis_client = WebsiteApiClient()
    return JsonResponse(redis_client.appointments_for_customer(customer_id))

def cancel_appointment(request, appointment_id):
    redis_client = WebsiteApiClient()
    return JsonResponse(redis_client.cancel_appointment([appointment_id]))


def temporal_appointments_for_customer(customer_id):
    return (
        {'appointments': [{'appointment_id': '714841L',
                   'display_string': '3:30 PM - 4:30 PM',
                   'end': dt.datetime(2022, 6, 7, 16, 30),
                   'start': dt.datetime(2022, 6, 7, 15, 30),
                   'store_id': u'TRPL09',
                   'VIN': None},
                  {'appointment_id': '714842L',
                   'display_string': '1:30 PM - 2:30 PM',
                   'end': dt.datetime(2022, 6, 7, 14, 30),
                   'start': dt.datetime(2022, 6, 7, 13, 30),
                   'store_id': u'TRPL09',
                   'VIN': '4YMBU1214MN020458'},
                   ],
        'customer_id': 1602019,
        'error': False,
        'total_appointments': 2}
    )

def temporal_cancel_appointment(appointment):
    return (
        # {'error': True, 'message': 'Failed to cancel appointment'}
        {'error': False, 'message': 'Appointment Canceled'}
    )

@csrf_exempt
def set_appointment(request):
    redis_client = WebsiteApiClient()
    req_body = request.body.decode()
    try:
        body = json.loads(req_body)
        appointment = json.loads(request.body.decode())['appointment_id']
        trailer_vin = json.loads(request.body.decode())['trailer_vin']
    except json.JSONDecodeError:
        return JsonResponse({'error': True, 'message': 'Error occurred, contact Customer Support'}, safe=False, status=500)

    trailer = Trailer.objects.select_related('store').prefetch_related('trailertranslation_set').get(vin=trailer_vin)
    trailer_verbose = trailer.trailertranslation_set.get(language=get_language().upper())
    full_lang = "English" if get_language().upper() == 'EN' else 'Spanish'

    customer_id = redis_client.get_or_create_customer(
        invoice_name= json.loads(request.body.decode())['customer']['first_name']+ ' ' + json.loads(request.body.decode())['customer']['last_name'],
        first_name= json.loads(request.body.decode())['customer']['first_name'],
        last_name= json.loads(request.body.decode())['customer']['last_name'],
        title=trailer_verbose.short_description,
        email_address= json.loads(request.body.decode())['customer']['email'],
        phone_number= json.loads(request.body.decode())['customer']['phone'],
        address_1="",
        address_2="",
        city= json.loads(request.body.decode())['store']['city'],
        state_short= json.loads(request.body.decode())['store']['state'],
        postal_code= json.loads(request.body.decode())['customer']['zipcode'],
        country='USA',
        language=full_lang,
    )
    #customer_id = 1;
    if customer_id:
        if not customer_id.get('error', False):
            appointments = redis_client.appointments_for_customer(customer_id['customer_id'])
        else:
            return JsonResponse({'error': True, 'message': 'General error'}, safe=False, status=500)
    else:
        return JsonResponse({'error': True, 'message': 'General error'}, safe=False, status=500)

    # Get appointments_for_customer 
    #appointments = temporal_appointments_for_customer(customer_id)
    # if more than 0 appointments
    if appointments['total_appointments'] > 0:
        ordered_appointments = sorted(appointments['appointments'], key=lambda ob: ob['start'])
        last_appointment = ordered_appointments[-1]
        # return last appointment
        return JsonResponse({'error': False, 'message': 'Appointment Exists', 'last_appointment': last_appointment }, safe=False)
    # If total appointments is 0
    else:
        return JsonResponse(redis_client.set_appointment_vin(appointment, customer_id['customer_id'], trailer_vin),safe=False)    
        #return JsonResponse({'error': False, 'message': 'Appointment set'}, safe=False)

@csrf_exempt
def set_service_appointment(request):
    redis_client = WebsiteApiClient()
    data = json.loads(request.body.decode())
    appointment = data['appointment_id']

    full_lang = "English" if get_language().upper() == 'EN' else 'Spanish'
    customer_id = redis_client.get_or_create_customer(
        invoice_name= data['customer']['first_name']+ ' ' + data['customer']['last_name'],
        first_name= data['customer']['first_name'],
        last_name= data['customer']['last_name'],
        title='Service',
        email_address= data['customer']['email'],
        phone_number= data['customer']['phone'],
        address_1="",
        address_2="",
        city= data['store']['city'],
        state_short= data['store']['state'],
        postal_code= data['customer']['zipcode'],
        country='USA',
        language=full_lang,
    )

    if not customer_id.get('error', False):
        appointments = redis_client.appointments_for_customer(customer_id['customer_id'])
    else:
        return JsonResponse({'error': True, 'message': 'General error'}, safe=False, status=500)

    if appointments['total_appointments'] > 0:
        last_service_appt = None
        for appointment in appointments['appointments']:
            if appointment['type'] == 'Service':
                last_service_appt = appointment

        if last_service_appt:
            return JsonResponse({'error': False, 'message': 'Appointment Exists', 'last_appointment': last_service_appt}, safe=False)
    response = redis_client.set_service_appointment(appointment, customer_id['customer_id'], data.get("service_type", ""))

    return JsonResponse(response,safe=False)

@csrf_exempt
def set_new_appointment(request):
    redis_client = WebsiteApiClient()
    try:
        appointment = json.loads(request.body.decode())['appointment_id']
        last_appointment = json.loads(request.body.decode())['last_appointment_id']
        trailer_vin = json.loads(request.body.decode())['trailer_vin']
    except json.JSONDecodeError:
        return JsonResponse({'error': True, 'message': 'Error occurred, contact Customer Support'}, safe=False, status=500)

    trailer = Trailer.objects.select_related('store').prefetch_related('trailertranslation_set').get(vin=trailer_vin)
    trailer_verbose = trailer.trailertranslation_set.get(language=get_language().upper())
    full_lang = "English" if get_language().upper() == 'EN' else 'Spanish'

    customer_id = redis_client.get_or_create_customer(
        invoice_name= json.loads(request.body.decode())['customer']['first_name']+ ' ' + json.loads(request.body.decode())['customer']['last_name'],
        first_name= json.loads(request.body.decode())['customer']['first_name'],
        last_name= json.loads(request.body.decode())['customer']['last_name'],
        title=trailer_verbose.short_description,
        email_address= json.loads(request.body.decode())['customer']['email'],
        phone_number= json.loads(request.body.decode())['customer']['phone'],
        address_1="",
        address_2="",
        city= json.loads(request.body.decode())['store']['city'],
        state_short= json.loads(request.body.decode())['store']['state'],
        postal_code= json.loads(request.body.decode())['customer']['zipcode'],
        country='USA',
        language=full_lang,
    )
    #customer_id = 1;

    # cancel appointment
    cancel_appoinment = redis_client.cancel_appointment(last_appointment)
    #cancel_appoinment = temporal_cancel_appointment(last_appointment)
    
    if cancel_appoinment['error'] == True:
        return JsonResponse({'error': True, 'message': 'Failed to cancel appointment'}, safe=False)

    return JsonResponse(redis_client.set_appointment_vin(appointment, customer_id['customer_id'], trailer_vin),safe=False)
    #return JsonResponse({'error': False, 'message': 'Appointment set'}, safe=False)

@csrf_exempt
def store_locations(request, state=''):
    locations, count = list_locations(state=state)

    return locations


class CustomCreate(CreateAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerializer
    permission_classes = [AllowAny]



class FleetCreate(CreateAPIView):
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer
    permission_classes = [AllowAny]



class TrailerVINValidation(RetrieveAPIView):
    queryset = Trailer.objects.all()
    lookup_field = 'vin'
    serializer_class = VINTrailerSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {'vin': self.kwargs['vin'], 'status': 150}
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj


class WarrantyCreate(CreateAPIView):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_serializer_context(self):
        cxt = super(WarrantyCreate, self).get_serializer_context()
        cxt.update({'request': self.request})
        return cxt


class WarrantyImages(CreateAPIView):
    queryset = WarrantyPhoto.objects.all()
    serializer_class = WarrantyPhotoSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def get_serializer_context(self):
        cxt = super().get_serializer_context()
        cxt.update({'request': self.request})
        return cxt


class TrailersCount(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        store_city = request.query_params.get('trailer-store', None)
        try:
            location = Location.objects.prefetch_related('trailer_set').get(store_city=store_city)
        except ObjectDoesNotExist:
            if store_city is not None:
                return Response({'trailer-store': f'Store "{store_city}" Does Not Exist'})
            else:
                return Response({'trailer-store': 'Required'})
        trailer_type = request.query_params.get('trailer-type', 'all')
        if trailer_type != 'all':
            trailers = get_store_trailers(location).filter(category__category_map__slug=trailer_type).count()
        else:
            trailers = get_store_trailers(location).count()
        return Response({'location': store_city, 'type': trailer_type, 'count': trailers})


class CartSession(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        session_id = request.POST.get('sessionid')
        # cart_item = request.POST.get('cart_item')
        cart_item = request.data['cart_item']
        request.session['cart_item'] = cart_item
        request.session.modified = True
        # session = SessionStore(session_key=session_id)
        # if session.pop('cart_item', False):
        #     status_code = 204
        # else:
        #     status_code = 201
        # session['cart_item'] = cart_item
        # session.save()
        return Response({session_id: {"cart_item": cart_item}}, status=201)

    def delete(self, request):
        session_id = request.POST.get('sessionid')
        try:
            del request.session['cart_item']
            request.session.modified = True
        except KeyError:
            pass
        # session = SessionStore(session_key=session_id)
        # session.pop('cart_item')
        # session.save()
        return Response({"Deleted successfully": 204}, status=204)


class UserLocation(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        session_id = request.POST.get('sessionid')
        # location_id = request.POST.get('location_id')
        location_id = request.data['location_id']
        request.session['user_location'] = location_id
        request.session.modified = True
        # session = SessionStore(session_key=session_id)
        # session.pop('user_location', None)
        # session['user_location'] = location_id
        # session.save()
        return Response({session_id: {"location_id": location_id}})


@csrf_exempt
@require_POST
def review_create(request):
    json_data = request.body
    data = json.loads(json_data)
    for event in data["events"]:
        save_review.delay(event["eventName"], event['eventData'])
    return HttpResponse(status=201)


class CheckoutViewTest(CreateAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    redis_conn = None
    def post(self, request, *args, **kwargs):
        data = request.data
        is_valid, errors = self.payload_is_valid(data)
        if not is_valid and errors:
            return Response(errors, status=400)
        try:
            logger.warning('--------- STARTING NEW TRANSACTION ------')
            redis_conn = WebsiteApiClient()
            logger.warning(f"{data=}")
            redis_language = 'Spanish' if get_language() == 'es' else 'English'
            logger.warning(f"{redis_language=}")
            trailer = Trailer.objects.select_related('store').prefetch_related('trailertranslation_set').get(
                vin=data['trailer_id'])
            logger.warning(f"{trailer=}")
            trailer_verbose = trailer.trailertranslation_set.get(language=get_language().upper()).short_description
            logger.warning(f"{trailer_verbose=}")
            try:
                customer_id = redis_conn.get_or_create_customer(
                    invoice_name=' '.join((data['firstname'], data['lastname'])),
                    first_name=data['firstname'],
                    last_name=data['lastname'],
                    title=trailer_verbose,
                    email_address=data['email'],
                    phone_number=data['phone'],
                    address_1=data.get('address', ''),
                    address_2=None,
                    city=data.get('city', ''),
                    state_short=data.get('state', ''),
                    postal_code=data['zip_code'],
                    country='USA',
                    language=redis_language
                )['customer_id']
            except KeyError:
                return Response( {'error': "Credit Card charge not made, please call Customer Support"}, status=500)
            logger.warning(f"{customer_id=}")
            trailer_status = redis_conn.trailer_status(data['trailer_id'])
            logger.warning(trailer_status)
            if int(trailer_status['status']) != 100:
                return Response(
                    {"error": f"Sorry this trailer is already {trailer_status['status_verbose'].lower()}"},
                    status=400)
            customer_active_reserves = int(redis_conn.customer_active_reserves(customer_id)['active_reserves'])
            if customer_active_reserves > 0:
                if customer_active_reserves == 1:
                    msg = f"""Error: You cannot reserve more than one trailer at a time. Please call {trailer.store.store_phone} 
                    to place a nonrefundable $250 deposit on this trailer to reserve it."""
                elif customer_active_reserves == 2:
                    msg = f"""Error: You cannot place more than two reservations within 90 days. Please call {trailer.store.store_phone} 
                    to place a nonrefundable $250 deposit on this trailer to reserve it."""
                return Response(
                    {"error": msg},
                    status=400
                )
            created_invoice = redis_conn.create_invoice(
                customer_id=customer_id,
                store_id=trailer.store.store_id,
                VIN=data['trailer_id']
            )
            logger.warning(f"{created_invoice=}")
            invoice_creation_error = bool(created_invoice.get('error', False))
            if invoice_creation_error:
                return Response(
                    {"error": created_invoice['message']},
                    status=400
                )
            invoice = redis_conn.invoice_data(created_invoice['store_id'], created_invoice['invoice_number'])
            customer_ip = get_ip_customer(request)
            payload = {
                'invoice': invoice,
                'transaction': {
                    'dataDescriptor': request.data['transaction']['dataDescriptor'],
                    'dataValue': request.data['transaction']['dataValue'],
                },
                'customer_ip': customer_ip,
                'email': request.data['email'],
                'amount': 1
            }
            payload['customer_type'] = "individual"
            logger.warning('Initializing payment process...')
            country = ip_country(request, customer_ip)
            authorize_response = authorizenet_process(payload, auth_only=True)
            logger.warning('logging response from Authorize')
            logger.warning(str(authorize_response))
            response_kwargs = self.post_process_charge(authorize_response, payload, trailer, request)
            logger.warning('Response kwargs from post_process_charge...')
            logger.warning(response_kwargs)
            return Response(**response_kwargs)
        except RuntimeError:
            return Response(
                {"error": "Ooops! Something went wrong"},
                status=409
            )
        except ValueError:
            # Are you trying to purchase from outside the US??
            return Response(
                {"error": "Error, please contact customer service at 877-850-7587"},
                status=409
            )

    def post_process_charge(self, response, payload, trailer, request):
        if response is not None:
            redis_conn = WebsiteApiClient()
            invoice = payload['invoice']
            # Check to see if the API request was successfully received and acted upon
            logger.warning(f'Got response code: {response.messages.resultCode}')
            if response.messages.resultCode == "Ok":
                response_code = response.transactionResponse.responseCode
                auth_code = response.transactionResponse.authCode
                trans_id = response.transactionResponse.transId
                # Since the API request was successful, look for a transaction response
                # and parse it to display the results of authorizing the card
                if hasattr(response.transactionResponse, 'messages'):
                    logger.warning('messages from Authorize transaction response')
                    logger.warning(response.transactionResponse.messages.message)
                    message = response.transactionResponse.messages.message[0].description
                    TestInvoice.objects.create(
                        invoice_id=invoice['InvoiceNumber'],
                        trailer=trailer,
                        customer_email=payload['email'],
                        date=dt.datetime.now()
                    )
                    request.session['last_invoice'] = invoice['InvoiceNumber']
                    try:
                        del request.session['cart_item']
                        request.session.modified = True
                    except KeyError:
                        pass
                    response_kwargs = {
                        'data': {
                            'message': response.transactionResponse.messages.message[0].description,
                            'bank_auth_code': response.transactionResponse.authCode,
                            'card_number': response.transactionResponse.accountNumber,
                            'card_brand': response.transactionResponse.accountType
                        }, 'status': 200
                    }
                    logger.warning('About to add reserve to redis...')
                    redis_conn.add_reserve_to_invoice(
                        trailer.store.store_id,
                        invoice['InvoiceNumber'],
                        str(response_code),
                        str(auth_code),
                        str(trans_id),
                        str(message))
                    logger.warning('After redis transaction.')
                else:
                    logger.warning('Failed Transaction.')
                    logger.warning('No messages attribute in response.transactionResponse')
                    response_code = response.messages.message[0]['code'].text
                    message = response.messages.message[0]['text'].text
                    auth_code = None
                    trans_id = None
                    if hasattr(response.transactionResponse, 'errors'):
                        logger.warning(response.transactionResponse.errors)
                        response_code = str(response.transactionResponse.errors.error[0].errorCode)
                        message = response.transactionResponse.errors.error[0].errorText
                        logger.warning('Error Code:  %s' % response_code)
                        logger.warning('Error Message: %s' % message)
                        response_kwargs = {
                            'data': {
                                'message': response.transactionResponse.errors.error[0].errorText,
                                'card_number': response.transactionResponse.accountNumber,
                                'card_brand': response.transactionResponse.accountType
                            }, 'status': 400
                        }
                    else:
                        logger.warning('No attribute errors in response.transactionResponse')
                        message = "Failed Transaction: No further detail from payment processor."
                        response_code = "None"
                    logger.warning('About to add reserve to redis with no messages attr...')
                    redis_conn.add_reserve_to_invoice(
                        trailer.store.store_id,
                        invoice['InvoiceNumber'],
                        str(response_code),
                        str(auth_code),
                        str(trans_id),
                        str(message))
                    logger.warning('After redis transaction with no messages attr...')
            # Or, logger.warning errors if the API request wasn't successful
            else:
                logger.warning('Failed Transaction.')
                if hasattr(response, 'transactionResponse') and hasattr(response.transactionResponse, 'errors'):
                    logger.warning('Error Code: %s' % str(response.transactionResponse.errors.error[0].errorCode))
                    logger.warning('Error Message: %s' % response.transactionResponse.errors.error[0].errorText)
                    response_kwargs = {
                        'data': {
                            'message': response.transactionResponse.errors.error[0].errorText,
                            'card_number': response.transactionResponse.accountNumber,
                            'card_brand': response.transactionResponse.accountType
                        }, 'status': 400
                    }
                else:
                    logger.warning('Error Code: %s' % response.messages.message[0]['code'].text)
                    logger.warning('Error Message: %s' % response.messages.message[0]['text'].text)
        else:
            logger.warning('Null Response.')
            response_kwargs = {
                'data': {'message': 'Null response from payment processor.'},
                'status': 400
            }
        return response_kwargs

    def payload_is_valid(self, payload):
        ser = ReserveSerializer(data=payload)
        if not ser.is_valid():
            return False, ser.errors
        else:
            return True, ser.validated_data
