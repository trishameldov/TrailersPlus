from django.urls import path, re_path
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

from . import views

router = routers.SimpleRouter()
router.register(r"locations", views.LocationViewSet, basename="locations")

urlpatterns = router.urls
urlpatterns += [
    path(
        "forms/lower_price", views.LowerPriceCreate.as_view(), name="Lower Price Form"
    ),
    path(
        "forms/appointment", views.AppointmentCreate.as_view(), name="Appointment Form"
    ),
    path("locations/<str:state>", views.store_locations, name="All Locations"),
    path("appointment/set/", views.set_appointment, name="Set Appointment"),
    path("service-appt/set/", views.set_service_appointment, name="Set Service Appointment"),
    path("appointment/<str:store>/<str:date>/", views.get_available_appointment, name="Appointment Available"),
    path("service-appt/services/<str:store_id>/", views.get_store_services, name="store_services"),
    path("service-appt/<str:store>/<str:date>/", views.get_available_service_appointment, name="Service Appointment Available"),
    path("service-appt/<int:zip_code>/", views.get_zip_stores, name="Stores by ZipCode"),
    path("forms/custom", csrf_exempt(views.CustomCreate.as_view()), name="Custom Trailer Form"),
    path("forms/fleet", csrf_exempt(views.FleetCreate.as_view()), name="Fleet Trailers Form"),
    path("forms/warranty/", views.WarrantyCreate.as_view(), name="Warranty Form"),
    path("trustpilot/", views.review_create, name="TrustPilot Webhook"),
    path("product_reviews/", views.ProductReviewsList.as_view(), name='Product Reviews'),
    path("count_trailers/", views.TrailersCount.as_view(), name='Trailers Count'),
    path("session_cart/", views.CartSession.as_view(), name="Session Cart"),
    path("user_location/", views.UserLocation.as_view(), name="Session User Location"),
    path("checkout-test/", views.CheckoutViewTest.as_view(), name="Checkout view"),
    re_path(r"warranty-vin-validation/(?P<vin>[A-HJ-NPR-Z0-9]{17})/$", views.TrailerVINValidation.as_view(), name="vin_validation"),
    path('warranty-images/', views.WarrantyImages.as_view(), name='images-warranty'),
    path("new-appointment/set/", views.set_new_appointment, name="Set new Appointment"),
    path("customer_appointments/<str:customer_id>/", views.get_customer_appointments, name="Customer Appointments"),
    path("appointment/cancel/<str:appointment_id>/", views.cancel_appointment, name="Cancel Appointment"),
]
