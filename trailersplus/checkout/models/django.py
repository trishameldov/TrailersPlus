from django.db import models
from product.models.django import Trailer


# class Customer(models.Model):
#     redis_id = models.CharField('Customer ID', max_length=25, unique=True)
#     company = models.CharField(max_length=50)
#     firstname = models.CharField(max_length=50)
#     lastname = models.CharField(max_length=50)
#     email = models.CharField(max_length=50)
#     phone = models.CharField(max_length=15)
#     address = models.CharField(max_length=80)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     zip_code = models.CharField(max_length=6)

def default_trailer():
    try:
        trailer = Trailer.objects.raw("""
            SELECT vin FROM product_trailer ORDER BY vin ASC LIMIT 1;
        """)
        return trailer[0].vin
    except IndexError:
        pass

class TestInvoice(models.Model):

    invoice_id = models.CharField('Invoice ID', max_length=25, null=True, blank=True)
    # customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True)
    trailer = models.ForeignKey(
        Trailer,
        on_delete=models.PROTECT,
        verbose_name='Trailer',
        null=True,
        default=default_trailer,
    )
    customer_email = models.EmailField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.pk} Test Invoice"

    class Meta:
        verbose_name = "Test Invoice"
        verbose_name_plural = "Test Invoices"


# class ReserveTransaction(models.Model):
#     # refId
#     invoice = models.OneToOneField(TestInvoice, on_delete=models.CASCADE)
#     # authCode
#     bank_auth_code = models.CharField('Card issuing bank auth code', max_length=7)
#     # transId
#     auth_net_trans = models.CharField('AuthorizeNet transId', max_length=25)
#     # accountNumber
#     card_number = models.CharField('Censored card number', max_length=17)
#     # accountType
#     card_brand = models.CharField('Card brand', max_length=12)
#     # responseCode
#     status = models.CharField('Status of the transaction', max_length=2)
