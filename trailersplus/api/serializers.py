import base64
from rest_framework import serializers
from django.utils.translation import get_language
from django.middleware.csrf import get_token

from trailersplus.utils.objects import work_hours_table
from trailersplus.utils.objects import get_time_ago
# from checkout.models import TestInvoice, ReserveTransaction, Customer
from product.models import Location, Trailer
from .models import LowerPrice, Appointment, Custom, Fleet, Warranty, ProductReviews, WarrantyPhoto


class ReserveSerializer(serializers.Serializer):
    firstname = serializers.CharField(min_length=3)
    lastname = serializers.CharField(min_length=3)
    trailer_id = serializers.CharField(min_length=17)
    email = serializers.EmailField()
    phone = serializers.CharField(min_length=10)
    zip_code = serializers.IntegerField(min_value=1000)


# class CustomerSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Customer
#         fields = [
#             'redis_id', 'company', 'firstname', 'lastname', 'email',
#             'phone', 'address', 'city', 'state', 'zip_code'
#         ]


# class InvoiceSerializer(serializers.ModelSerializer):
#     customer = CustomerSerializer()

#     class Meta:
#         model = TestInvoice
#         fields = ['invoice_id', 'customer', 'trailer', 'customer_email', 'date']


# class ReserveTransactionSerializer(serializers.ModelSerializer):
#     invoice = InvoiceSerializer()

#     class Meta:
#         model = ReserveTransaction
#         fields = [
#             'invoice', 'bank_auth_code', 'auth_net_trans',
#             'card_number', 'card_brand', 'status',
#         ]


class LocationSerializer(serializers.ModelSerializer):
    store_link = serializers.SerializerMethodField()
    store_inventory_link = serializers.SerializerMethodField()
    state_long = serializers.SerializerMethodField()
    store_directions = serializers.SerializerMethodField()
    work_hours = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = [
            "store_id",
            "state",
            "state_long",
            "store_name",
            "store_city",
            "store_address",
            "store_zip",
            "store_directions",
            "store_email",
            "store_map_url",
            "store_phone",
            "store_keywords",
            "store_lat",
            "store_long",
            "store_description",
            "store_title",
            "work_hours",
            "store_link",
            "store_inventory_link",
        ]

    def get_store_link(self, obj):
        request = self.context["request"]
        return f"{request.scheme}://{request.site_name}/{obj.get_slug()}/"

    def get_store_inventory_link(self, obj):
        request = self.context["request"]
        return f"{request.scheme}://{request.site_name}/{obj.get_slug()}/inventory/"

    def get_state_long(self, obj):
        return obj.get_state_display()

    def get_store_directions(self, obj):
        locale = self.context["locale"]
        if locale == "es":
            return obj.store_spanish_directions
        return obj.store_directions

    def _group_and_capitalize(self, data):
        if data[1] is None:
            return data[0].capitalize()
        else:
            return f"{data[0].replace('_hours', '').capitalize()} - {data[1].capitalize()}"

    STORE_WORK_HOURS_TRANSLATION = {
        'Closed': 'Cerrado',
        'Set Appointment': 'Programar Cita',
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo',
    }

    def get_work_hours(self, obj):
        locale = self.context["locale"].lower()
        table_content = work_hours_table(obj.work_hours,
                                self.STORE_WORK_HOURS_TRANSLATION,
                                self._group_and_capitalize,
                                locale)
        table_body = f'<tbody> {table_content} </tbody>'
        return table_body


class LowerPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LowerPrice
        fields = ("url", "first_name", "last_name", "email", "phone", "zip", "trailer")


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ("first_name", "last_name", "email", "phone", "trailer")
    
    def create(self, validated_data: dict):
        validated_data.update({'language': get_language()})
        return super(AppointmentSerializer, self).create(validated_data)


class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Custom
        fields = (
            "name",
            "email",
            "zip",
            "description",
            "phone",
            "quantity",
            "trailer_type",
            "trailer_length",
            "store_id",
        )


class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = (
            "name",
            "email",
            "zip_code",
            "phone",
            "excepted_fleet",
            "description",
            "trailer_type",
            "trailer_length",
            "store_id",
        )


class VINTrailerSerializer(serializers.ModelSerializer):
    vin = serializers.CharField(read_only=True)

    class Meta:
        model = Trailer
        fields = ("vin",)


class BinaryField(serializers.Field):

    def to_representation(self, value):
        return base64.b64encode(value)

    def to_internal_value(self, data):
        return base64.b64decode(data)


class WarrantyPhotoSerializer(serializers.ModelSerializer):
    image = BinaryField(allow_null=False)

    def to_representation(self, instance):
        response_dict = super().to_representation(instance)
        response_dict['csrfmiddlewaretoken'] = get_token(self.context['request'])
        return response_dict

    class Meta:
        model = WarrantyPhoto
        fields = ('pk', 'warranty', 'image')


class WarrantySerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        response_dict = super().to_representation(instance)
        response_dict['csrfmiddlewaretoken'] = get_token(self.context['request'])
        return response_dict

    class Meta:
        model = Warranty
        fields = ("pk", "name", "email", "phone", "trailer", "description")


class ProductReviewsSerializer(serializers.ModelSerializer):
    created_ago = serializers.SerializerMethodField()

    class Meta:
        model = ProductReviews
        fields = ('title', 'content', 'stars', 'created_ago', 'author')

    def get_created_ago(self, obj):
        return get_time_ago(obj.created_at)
