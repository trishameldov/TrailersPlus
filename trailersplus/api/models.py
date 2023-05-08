from django.conf import settings
from django.utils import timezone
from django.db import models
from product.models import Trailer
from django.contrib.postgres.fields import JSONField
from product.models.django import Location


class LowerPrice(models.Model):
    url = models.CharField(max_length=250)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=45)
    zip = models.CharField(max_length=5, blank=True, null=True)
    copied = models.BooleanField(default=False)
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE)
    language = models.CharField(
        max_length=2,
        choices=(('en', 'English'), ('es', 'Spanish')), default='en')
    created_at = models.DateTimeField(auto_now_add=True)


class Appointment(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=45)

    language = models.CharField(max_length=2, choices=(('en', 'English'), ('es', 'Spanish')), default='en')
    copied = models.BooleanField(default=False)

    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)


class Custom(models.Model):
    name = models.CharField(max_length=180)
    email = models.EmailField()
    zip = models.CharField(max_length=5, blank=True, null=True)
    description = models.TextField()
    phone = models.CharField(max_length=45, blank=True, null=True)
    quantity = models.CharField(max_length=64, blank=True, null=True)
    trailer_type = models.CharField(max_length=45, blank=True, null=True)
    trailer_length = models.CharField(max_length=45, blank=True, null=True)
    store_id = models.CharField(max_length=45, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def report(self):
        properties = {
            "Name": self.name,
            "Email": self.email,
            "Zip Code": self.zip,
            "Phone": self.phone,
            "Number of Trailers Needed": self.quantity,
            "Trailer Type": self.trailer_type,
            "Trailer Length": self.trailer_length,
            "Store ID": self.store_id,
            "Created At": self.created_at.strftime("%m/%d/%y %H:%M"),
            "Description": self.description,
        }

        if self.quantity is None:
            del properties["Number of Trailers Needed"]

        return '\n'.join([f'{key}: {value}' for key, value in properties.items()])


class Warranty(models.Model):
    name = models.CharField(max_length=180, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    trailer = models.ForeignKey(Trailer, on_delete=models.CASCADE)
    description = models.TextField()
    photo_desc = models.TextField()
    update_at = models.DateTimeField()
    created_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.update_at = timezone.now()
        return super(Warranty, self).save(*args, **kwargs)


def image_path(instance, filename):
    return f"{instance.vin}/{filename}"


class WarrantyPhoto(models.Model):
    warranty = models.ForeignKey(Warranty, on_delete=models.CASCADE)
    image = models.BinaryField(blank=True, null=True, editable=True)


class Fleet(models.Model):
    name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=45)
    zip_code = models.CharField(max_length=5, blank=True, null=True)
    excepted_fleet = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField()
    trailer_type = models.CharField(max_length=45, blank=True, null=True)
    trailer_length = models.CharField(max_length=45, blank=True, null=True)
    store_id = models.CharField(max_length=45, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def report(self):
        properties = {
            "Name": self.name,
            "Email": self.email,
            "Zip Code": self.zip_code,
            "Phone": self.phone,
            "Number of Trailers Needed": self.excepted_fleet,
            "Trailer Type": self.trailer_type,
            "Trailer Length": self.trailer_length,
            "Store ID": self.store_id,
            "Created At": self.created_at.strftime("%m/%d/%y %H:%M"),
            "Description": self.description,
        }

        if self.excepted_fleet is None:
            del properties["Number of Trailers Needed"]

        return '\n'.join([f'{key}: {value}' for key, value in properties.items()])

class ServiceReviews(models.Model):
    comment_id = models.CharField(max_length=26, primary_key=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    stars = models.IntegerField()
    created_at = models.DateTimeField()
    author = models.CharField(max_length=50)
    data_raw = JSONField()

    def __str__(self):
        return f"{self.author} Service Review"

    class Meta:
        ordering = ["-created_at"]


class ProductReviews(models.Model):
    comment_id = models.CharField(max_length=26, primary_key=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    stars = models.IntegerField()
    created_at = models.DateTimeField()
    author = models.CharField(max_length=120)
    products = models.ManyToManyField(Trailer, related_name="reviews")
    data_raw = JSONField()

    def __str__(self):
        return f"{self.author} Review"

    class Meta:
        ordering = ["-created_at"]


class TrustpilotCount(models.Model):
    sku = models.CharField(max_length=255, primary_key=True)
    count = models.IntegerField(default=0)
