import logging
import json
import requests
from decimal import Decimal
from datetime import date

import ujson

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.views.decorators.csrf import csrf_exempt

from trailersplus.celery import app
from trailersplus.utils.celery import wait_for_result
from product.models.django import Trailer
from .forms import InvoiceForm
from .models.django import TestInvoice
from .models import CheckoutPage
from product.models.django import Location
from datetime import datetime, date
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView
from django.http import HttpResponse, Http404, JsonResponse

from .services import WebsiteApiClient, authorizenet_process
from authorizenet import apicontractsv1
from authorizenet.constants import constants
from authorizenet.apicontrollers import createTransactionController
from django.conf import settings
from api.utils import get_ip_customer

from uuid import uuid4


logger = logging.getLogger(__name__)


def redirect_checkout_vin(request, trailer_id):
    """
    Redirects to the CheckoutPage if the user entered the checkout url with
    the ID of a trailer.
    """

    checkout_page = CheckoutPage.objects.first()
    slug = checkout_page.slug
    checkout_url = f"/{slug}/?vin={trailer_id}"

    return redirect(checkout_url)

def prer_submit(request):
    try:
        redis_client = WebsiteApiClient()
        trailer = Trailer.objects.select_related('store').prefetch_related('trailertranslation_set').get(
            vin=request.POST['trailer_id'])
        trailer_verbose = trailer.trailertranslation_set.get(language=get_language().upper())
        full_lang = "English" if get_language().upper() == 'EN' else 'Spanish'
        customer_id = redis_client.get_or_create_customer(
            invoice_name=request.POST["company"] if request.POST["company"] else request.POST['firstname'] + '_' +
                                                                                 request.POST['lastname'],
            first_name=request.POST['firstname'],
            last_name=request.POST['lastname'],
            title=trailer_verbose.short_description,
            email_address=request.POST['email'],
            phone_number=request.POST['phone'],
            address_1=request.POST['address'],
            address_2=request.POST['address'],
            city=request.POST['city'],
            state_short=request.POST['state'],
            postal_code=request.POST['zip'],
            country='USA',
            language=full_lang,
        )
        try:
            customer_id = customer_id['customer_id']
        except KeyError:
            customer_id = uuid4()
        trailer_status = redis_client.trailer_status(request.POST['trailer_id'])
        try:
            trailer_status = trailer_status['status']
        except KeyError:
            trailer_status = 100
        customer_active_reserver = redis_client.customer_active_reserves(customer_id)
        try:
            customer_active_reserver = customer_active_reserver['active_reserves']
        except KeyError:
            customer_active_reserver = 0
        if trailer_status != 100 or customer_active_reserver:
            return redirect('/')
        store_id = trailer.store.store_id
        new_invoice = redis_client.create_invoice(customer_id, store_id, trailer.vin)
        try:
            if new_invoice['error']:
                return redirect('/')
            invoice_number = new_invoice['invoice_number']
        except KeyError:
            invoice_number = uuid4()

        # FAKE TRANSACTION BLOCK

        redis_client.add_reserve_to_invoice()

        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZE_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZE_TRANSACTION_KEY

        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = request.POST['cardnumber']
        expirity = request.POST['expirity'].split('/')
        creditCard.expirationDate = f"20{expirity[1]}-{expirity[0]}"
        creditCard.cardCode = request.POST['ccv']

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        order = apicontractsv1.orderType()
        order.invoiceNumber = invoice_number
        order.description = trailer_verbose.short_description

        customerAddress = apicontractsv1.customerAddressType()
        customerAddress.firstName = request.POST['firstname']
        customerAddress.lastName = request.POST['lastname']
        customerAddress.company = request.POST['company']
        customerAddress.address = request.POST['address']
        customerAddress.city = request.POST['city']
        customerAddress.state = request.POST['state']
        customerAddress.zip = request.POST['zip']
        customerAddress.country = "USA"

        customerData = apicontractsv1.customerDataType()
        customerData.type = "company" if request.POST['company'] else "individual"
        customerData.id = customer_id
        customerData.email = request.POST['email']

        duplicateWindowSetting = apicontractsv1.settingType()
        duplicateWindowSetting.settingName = "duplicateWindow"
        duplicateWindowSetting.settingValue = "600"
        settings = apicontractsv1.ArrayOfSetting()
        settings.setting.append(duplicateWindowSetting)

        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authOnlyTransaction"
        transactionrequest.amount = 50
        transactionrequest.payment = payment
        transactionrequest.order = order
        transactionrequest.billTo = customerAddress
        transactionrequest.customer = customerData
        transactionrequest.transactionSettings = settings

        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId = "TrailersPlus"
        createtransactionrequest.transactionRequest = transactionrequest

        createtransactioncontroller = createTransactionController(
            createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()

        if response is not None:
            _res = redis_client.add_reserve_to_invoice(store_id,
                                                       invoice_number,
                                                       response.messages.resultCode,

                                                       response.transactionResponse.transId,
                                                       response.mesages.message)
            try:
                if not _res['error']:
                    return HttpResponse(b"SUCCESS", status=200)
            except KeyError:
                return HttpResponse(b"SUCCESS", status=200)
        return HttpResponse(b"Authorize payment failed", status=400)
    except RuntimeError:
        return HttpResponse(b"Failed, Redis connection timeout", status=400)
    except Exception as e:
        error = {
            "status": 400,
            "error": True,
            "error_text": str(e)
        }
        return HttpResponse(ujson.dumps(error), status=400)


def lxml_to_dict(response):
    result = {k: lxml_to_dict(v) for k, v in response.__dict__.items()}
    if not len(result):
        return str(response)
    else:
        return result


def submit(request):
    trailer = Trailer.objects.select_related('store').prefetch_related('trailertranslation_set').get(
        vin=request.POST['trailer_id'])
    trailer_verbose = trailer.trailertranslation_set.get(language=get_language().upper())
    invoice_number = str(uuid4())[:10]
    customer_id = str(uuid4())[:10]
    try:
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = settings.AUTHORIZE_LOGIN_ID
        merchantAuth.transactionKey = settings.AUTHORIZE_TRANSACTION_KEY

        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = request.POST['cardnumber'].replace('-', '')
        expirity = request.POST['expirity'].split('/')
        creditCard.expirationDate = f"20{expirity[1]}-{expirity[0]}"
        creditCard.cardCode = request.POST['ccv']

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        order = apicontractsv1.orderType()
        order.invoiceNumber = invoice_number  ###)[:10]
        order.description = trailer_verbose.short_description

        customerAddress = apicontractsv1.customerAddressType()
        customerAddress.firstName = request.POST['firstname']
        customerAddress.lastName = request.POST['lastname']
        customerAddress.company = request.POST['company']
        customerAddress.address = request.POST['address']
        customerAddress.city = request.POST['city']
        customerAddress.state = request.POST['state']
        customerAddress.zip = request.POST['zip']
        customerAddress.country = "USA"

        customerData = apicontractsv1.customerDataType()
        customerData.type = "business" if request.POST['company'] else "individual"
        customerData.id = customer_id  ###
        customerData.email = request.POST['email']

        duplicateWindowSetting = apicontractsv1.settingType()
        duplicateWindowSetting.settingName = "duplicateWindow"
        duplicateWindowSetting.settingValue = "600"
        settings_array = apicontractsv1.ArrayOfSetting()
        settings_array.setting.append(duplicateWindowSetting)

        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authOnlyTransaction"
        transactionrequest.amount = 50
        transactionrequest.payment = payment
        transactionrequest.order = order
        transactionrequest.billTo = customerAddress
        transactionrequest.customer = customerData
        transactionrequest.transactionSettings = settings_array

        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        createtransactionrequest.refId = "TrailersPlus"
        createtransactionrequest.transactionRequest = transactionrequest

        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()
        if response is not None:
            return HttpResponse(ujson.dumps({
                "authorize": lxml_to_dict(response),
                "data": dict(request.POST)
            }))
        else:
            return HttpResponse(b"Can't get response from Authorize.net")
    except Exception as e:
        return HttpResponse(ujson.dumps({"error": repr(e)}))


class InvoiceView(FormView):
    template_name = "invoice_template.html"
    form_class = InvoiceForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(InvoiceView, self).dispatch(request, *args, **kwargs)

    def get(self, request, invoice_id, *args, **kwargs):
        form_class = self.get_form_class()
        form: InvoiceForm = self.get_form(form_class)
        context = self.get_context_data(form=form, invoice_id=invoice_id)
        context["AUTHORIZE_CLIENT_KEY"] = settings.AUTHORIZE_CLIENT_KEY
        context["AUTHORIZE_LOGIN_ID"] = settings.AUTHORIZE_LOGIN_ID
        context["AUTHORIZE_JS_URL"] = settings.AUTHORIZE_JS_URL
        return self.render_to_response(context)

    def post(self, request, invoice_id, *args, **kwargs):
        form_class = self.get_form_class()
        form: InvoiceForm = self.get_form(form_class)
        context = self.get_context_data(form=form, invoice_id=invoice_id)
        invoice_data = context['invoice']

        try:
            customer_email = TestInvoice.objects.get(
                invoice_id=invoice_data['InvoiceNumber'],
                trailer__vin=invoice_data['VIN'],
                trailer__store__store_id=invoice_data['StoreID']
            ).customer_email
        except TestInvoice.DoesNotExist:
            customer_email = 'example@example.com'
        form_valid = form.is_valid()
        if form_valid and not context['payment_status']:
            logger.warning('Form is valid')
            client = WebsiteApiClient()
            context.update(
                {"additional": {"success": False, "invalid_form": False}}
            )
            if form.cleaned_data['payment_type'] == 'full':
                amount = context['limits']['max']
            else:
                amount = form.cleaned_data['partial_value']
            customer_ip = get_ip_customer(request)
            payload = {
                'invoice': invoice_data,
                'transaction': {
                    'dataDescriptor': form.cleaned_data['data_descriptor'],
                    'dataValue': form.cleaned_data['data_value'],
                },
                'customer_ip': customer_ip,
                'email': customer_email,
                'customer_type': 'individual',
                'amount': amount,
            }
            try:
                response = authorizenet_process(payload)
                if response:
                    if hasattr(response, 'transactionResponse'):
                        response_code = response.transactionResponse.responseCode
                        auth_code = response.transactionResponse.authCode
                        trans_id = response.transactionResponse.transId
                        client_type = response.transactionResponse.accountType
                        if hasattr(response.transactionResponse, 'messages'):
                            message = response.transactionResponse.messages.message[0].description
                            context.update(
                                {"additional": {"success": True, "invalid_form": False}}
                            )
                        else:
                            message = response.transactionResponse.errors.error[0].errorText
                            context.update(
                                {"additional": {"success": False, "error": message, "invalid_form": False}}
                            )
                        client.add_payment_to_invoice(str(invoice_data['StoreID']),
                                                      int(invoice_data['InvoiceNumber']),
                                                      float(amount),
                                                      str(client_type),
                                                      str(response_code),
                                                      str(auth_code),
                                                      str(trans_id),
                                                      str(message))
                    else:
                        response_code = response.messages.message[0]['code'].text
                        message = response.messages.message[0]['text'].text
                        auth_code = None
                        trans_id = None
                        client.add_payment_to_invoice(str(invoice_data['StoreID']),
                                                      int(invoice_data['InvoiceNumber']),
                                                      float(amount),
                                                      None,
                                                      str(response_code),
                                                      auth_code,
                                                      trans_id,
                                                      str(message))
                        context.update(
                            {"additional": {"success": False, "error": message, "invalid_form": False}}
                        )
            except Exception as e:
                context.update(
                    {
                        "additional": {
                            "success": False,
                            "error": "Something went wrong. no charge made.",
                            "invalid_form": False,
                            "response_message": "Unknown error, no charge made."
                        }
                    }
                )
        elif not form_valid:
            logger.warning('Invalid form')
            context.update({
                'additional': {
                    'success': False,
                    'invalid_form': True,
                }
            })
        else:
            logger.warning('Atempt to pay an invoice already paid.')
            context.update(
                {
                    "additional": {
                        "success": False,
                        "error": "Invoice was alread paid",
                        "invalid_form": False,
                        "response_message": "Invoice already, no charge made."
                    }
                }
            )
        return self.render_to_response(context)

    def invoice_is_paid(self, invoice_data):
        lines = invoice_data.get('lines')
        for line in lines:
            if line['PartNumber'] == 'PAYMENT' or line['PartNumber'] == 'POSTEDPMNT':
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super(InvoiceView, self).get_context_data(**kwargs)
        client = WebsiteApiClient()
        invoice_from_link = client.invoice_from_link(kwargs.get('invoice_id'))
        try:
            error = invoice_from_link['error']
        except KeyError:
            pass
        else:
            if error:
                raise Http404
        payment_status = self.invoice_is_paid(invoice_from_link)
        invoice = client.invoice_data(invoice_from_link['StoreID'], invoice_from_link['InvoiceNumber'])
        limits = client.invoice_payment_limits(invoice_from_link['StoreID'], invoice_from_link['InvoiceNumber'])
        try:
            serial_number = invoice['lines'][0]['SerialNumber']
        except KeyError:
            serial_number = None
        context.update(
            {
                "invoice": invoice,
                "VIN": serial_number,
                "limits": limits,
                "payment_status": payment_status,
                "qty": 1,
                "transaction_date": date.today(),
                "subTotal": sum(line['ExtendedCost'] for line in invoice['lines'] if line['PartNumber'] != 'SALESTAX'),
                "balance": float(invoice['InvoiceValue']) - float(invoice['Collected']),
                "additional": {"success": None, "invalid_form": None},
            }
        )
        context.update({
            "subTotal": sum(line['ExtendedCost'] for line in invoice['lines'] if line['PartNumber'] != 'SALESTAX'),
            "balance": float(invoice['InvoiceValue']) - float(invoice['Collected'])
        })
        context.update({
            "additional": {"success": None, "invalid_form": None}
        })
        context['ach_enabled'] = settings.ACH_ENABLED
        try:
            location = Location.objects.get(store_id=invoice_from_link['StoreID'])
        except Location.DoesNotExist:
            location = Location.objects.first()
        context['UTA_MERCHANTNO'] = location.uta_merchant
        return context

@csrf_exempt
def invoice_payment_ach(request):
    client = WebsiteApiClient()
    # uuid_num = client.invoice_data(json.loads(request.body.decode())['StoreID'],json.loads(request.body.decode())['InvoiceNumber'])
    endpoint = settings.PAYMENT_ENDPOINT
    formdata = {
        # "USER": settings.PAYMENT_USER,
        # "PASSWORD": settings.PAYMENT_PASS,
        # "MERCHANTNO": settings.PAYMENT_MERCHANTNO,
        # "CUSTOMERNO": json.loads(request.body.decode())['StoreID']+"-"+json.loads(request.body.decode())['InvoiceNumber'],
        # "TRANSACTIONDATE": date.today().strftime("%m-%d-%y"),
        # "POST":settings.PAYMENT_POST,
        # "REDIRECT": "https://www.Trailersplus.com"
        "USER":json.loads(request.body.decode())["USER"],
        "PASSWORD":json.loads(request.body.decode())["PASSWORD"],
        "MERCHANTNO":json.loads(request.body.decode())["MERCHANTNO"],
        "CUSTOMERNO":json.loads(request.body.decode())["CUSTOMERNO"],
        "CUSTOMERNAME":json.loads(request.body.decode())["CUSTOMERNAME"],
        "PHONE":json.loads(request.body.decode())["PHONE"],
        "MEMO":json.loads(request.body.decode())["MEMO"],
        "AMOUNT":json.loads(request.body.decode())["AMOUNT"],
        "TRANSACTIONDATE":json.loads(request.body.decode())["TRANSACTIONDATE"],
        "REDIRECT":json.loads(request.body.decode())["REDIRECT"],
        "POST":json.loads(request.body.decode())["POST"]
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return HttpResponse(requests.post(endpoint, data=formdata, headers=headers))
    # return JsonResponse(requests.post(endpoint, data=formdata, headers=headers),safe=False)


