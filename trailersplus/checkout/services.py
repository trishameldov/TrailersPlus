import functools
import logging
from os import path
from uuid import uuid4

import ujson as json  # use this library from pip - it will take care of the datetime serialization and everything
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
from authorizenet.constants import constants
from django.conf import settings
from redis import StrictRedis

from .models import TestInvoice
from product.models.django import Trailer
import datetime as dt

logger = logging.getLogger(__name__)
REDIS_CONN_STRING = settings.REDIS_MESSAGE
COMMAND_QUEUE = 'WEBSITE_API_CLIENT'
RESPONSE_TIMEOUT = 30  # 30 seconds
REDIS_CA_CERT = settings.ROOT('trailersplus', 'certs', 'redis', 'aiven_ca.pem', required=True)


def authorizenet_process(payload, auth_only=False):
    """
    {
    'invoice': {
        'customer_data': {
          'first_name': 'John',
          'last_name': 'Doe',
          'invoice_name': 'My Comany, Inc',
          'line1': 'Reboroujo 208',
          'state_short': 'AZ',
          'postal_code': '90210'
        },
        'CashPriceInvoice': 0,
        'Collected': Decimal('0.00'),
        'CompleteDate': None,
        'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
        'CustomerID': '1697723L',
        'CustomerName': u'JOHN WATSON',
        'CustomerPicture': None,
        'DiscountedTrailer': Decimal('7249.00'),
        'Due': Decimal('7249.00'),
        'EditDate': datetime.datetime(2020, 11, 10, 12, 51, 56),
        'InvoiceNumber': '32047L',
        'InvoiceValue': Decimal('7249.00'),
        'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
        'SalesPerson2Active': None,
        'SalesPerson2Email': None,
        'SalesPerson2LoginID': None,
        'SalesPerson2Name': None,
        'SalesPerson2Number': None,
        'SalesPerson2UserID': None,
        'SalesPersonActive': 0,
        'SalesPersonEmail': None,
        'SalesPersonLoginID': u'TRAILERSPLUS\\weblead',
        'SalesPersonName': u'Web Lead',
        'SalesPersonNumber': u'0',
        'SalesPersonUserID': u'weblead',
        'Status': 1,
        'StatusDescription': u'Quote',
        'StoreID': u'TRPL35',
        'VIN': None,
        'lines': [{
          'CompleteDate': None,
          'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
          'Description': u'7 x 16 Loadrunner 7K',
          'EditDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
          'ExtendedCost': Decimal('10509.00'),
          'InvoiceDate': None,
          'InvoiceNumber': '32047L',
          'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
          'PartNumber': u'ILRD716TA2',
          'QtyDelivered': Decimal('1.00'),
          'QtyOrdered': Decimal('1.00'),
          'SerialNumber': u'4RALS1623MK075899',
          'StoreID': u'TRPL35',
          'Taxable': 0,
          'UniqueID': '25301348L',
          'UnitCost': Decimal('10509.00'),
          'Units': u'EACH'},
         {'CompleteDate': None,
          'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
          'Description': u'Dealer Discount Pre-approved',
          'EditDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
          'ExtendedCost': Decimal('-3260.00'),
          'InvoiceDate': None,
          'InvoiceNumber': '32047L',
          'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
          'PartNumber': u'DISCOUNT',
          'QtyDelivered': Decimal('1.00'),
          'QtyOrdered': Decimal('1.00'),
          'SerialNumber': None,
          'StoreID': u'TRPL35',
          'Taxable': 0,
          'UniqueID': '25301349L',
          'UnitCost': Decimal('-3260.00'),
          'Units': u'EACH'},
         {'CompleteDate': None,
          'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
          'Description': u'Sale price Approved By luteyns Approved Sale Price HD Coupler Lock Required On The Lot',
          'EditDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
          'ExtendedCost': Decimal('0.00'),
          'InvoiceDate': None,
          'InvoiceNumber': '32047L',
          'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
          'PartNumber': u'NOTE',
          'QtyDelivered': Decimal('1.00'),
          'QtyOrdered': Decimal('1.00'),
          'SerialNumber': None,
          'StoreID': u'TRPL35',
          'Taxable': 0,
          'UniqueID': '25301350L',
          'UnitCost': Decimal('0.00'),
          'Units': u'EACH'}]
    },
      "transaction": {
        "dataDescriptor": "sometext",
        "dataValue": "someothertext"
      },
      "email": "hi@example.com",
      "customer_type": "individual",
      "amount": Decimal('50393')
    }
    """
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = settings.AUTHORIZE_LOGIN_ID
    merchantAuth.transactionKey = settings.AUTHORIZE_TRANSACTION_KEY

    # Create the payment object for a payment nonce
    opaqueData = apicontractsv1.opaqueDataType()
    opaqueData.dataDescriptor = payload['transaction']['dataDescriptor']
    opaqueData.dataValue = payload['transaction']['dataValue']

    # Add the payment data to a paymentType object
    payment = apicontractsv1.paymentType()
    payment.opaqueData = opaqueData
    invoice_data = payload['invoice']
    order = apicontractsv1.orderType()
    order.invoiceNumber = f"{invoice_data['StoreID']}-{invoice_data['InvoiceNumber']}"  ###)[:10]
    order.description = f"{invoice_data['CustomerName']} {invoice_data['StoreID']}-{invoice_data['InvoiceNumber']} invoice"

    customerAddress = apicontractsv1.customerAddressType()
    customerAddress.firstName = invoice_data['customer_data'][0]['first_name']
    customerAddress.lastName = invoice_data['customer_data'][0]['last_name']
    customerAddress.address = invoice_data['customer_data'][0]['line1']
    customerAddress.city = invoice_data['customer_data'][0]['city']
    customerAddress.state = invoice_data['customer_data'][0]['state_short']
    customerAddress.zip = invoice_data['customer_data'][0]['postal_code']
    customerAddress.country = "USA"

    customerData = apicontractsv1.customerDataType()
    customerData.type = payload['customer_type']
    customerData.id = str(invoice_data['CustomerID'])
    customerData.email = payload['email']

    duplicateWindowSetting = apicontractsv1.settingType()
    duplicateWindowSetting.settingName = "duplicateWindow"
    duplicateWindowSetting.settingValue = "600"
    settings_array = apicontractsv1.ArrayOfSetting()
    settings_array.setting.append(duplicateWindowSetting)

    line_items = apicontractsv1.ArrayOfLineItem()
    for line in invoice_data['lines']:
        authorize_item = apicontractsv1.lineItemType()
        authorize_item.itemId = str(line['UniqueID'])
        authorize_item.name = str(line['PartNumber'])
        authorize_item.description = line['Description']
        authorize_item.quantity = str(line['QtyOrdered'])
        if float(line['UnitCost']) > 0:
            authorize_item.unitPrice = str(line['UnitCost'])
        else:
            authorize_item.discountAmount = str(line['UnitCost'])
    transactionrequest = apicontractsv1.transactionRequestType()
    if auth_only:
        transactionrequest.transactionType = "authOnlyTransaction"
    else:
        transactionrequest.transactionType = "authCaptureTransaction"
    transactionrequest.amount = str(payload['amount'])
    transactionrequest.payment = payment
    transactionrequest.order = order
    transactionrequest.billTo = customerAddress
    transactionrequest.customer = customerData
    transactionrequest.transactionSettings = settings_array
    transactionrequest.lineItems = line_items
    transactionrequest.customerIP = str(payload['customer_ip'])

    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId = "TrailersPlus"
    createtransactionrequest.transactionRequest = transactionrequest

    createtransactioncontroller = createTransactionController(createtransactionrequest)
    env = constants.PRODUCTION if not settings.DEBUG else constants.SANDBOX
    logger.warning(f'Environment {env}')
    createtransactioncontroller.setenvironment(env)
    createtransactioncontroller.execute()
    logger.warning('About to getresponse')
    return createtransactioncontroller.getresponse()


def production_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if settings.ALLOW_AUTHORIZENET:
            return func(*args, **kwargs)
        else:
            logger.warning("Non Production environment, dry run")
    return wrapper


class WebsiteApiClient(object):

    def __init__(self):
        self.redis = StrictRedis.from_url(REDIS_CONN_STRING, ssl_ca_certs=REDIS_CA_CERT)

    def _make_call(self, function, arguments):
        import pprint
        logger.warning("Strarting redis call")
        logger.warning("Generating key")
        key = str(uuid4())
        logger.warning(f"{key=}")
        logger.warning(f"Pushing {function=} with next args")
        logger.warning(arguments)
        self.redis.rpush(COMMAND_QUEUE, json.dumps({'function': function, 'args': arguments, 'key': key}))
        logger.warning("W8ting for response")
        data = self.redis.blpop(key, RESPONSE_TIMEOUT)
        if not data:
            raise RuntimeError('Timeout - No response from redis api')
        data = json.loads(data[1])
        logger.warning('Got response from redis:')
        logger.warning(data)
        return data

    def trailer_status(self, VIN):
        """ example return data
        {u'status': 150, u'status_verbose': u'Sold'}
        """
        return self._make_call('trailer_status', [VIN])

    @production_only
    def get_or_create_customer(self, invoice_name, first_name, last_name, title, email_address, phone_number,
                               address_1, address_2, city, state_short, postal_code, country, language='English'):
        """ language is 'English' or 'Spanish'
        invoice_name is either company name or customer full name
        example return data
        {'customer_id': cust_id}
        """
        return self._make_call(
            'get_or_create_customer',
            [invoice_name, first_name, last_name, title, email_address, phone_number,
             address_1, address_2, city, state_short, postal_code, country, language]
        )

    def customer_active_reserves(self, customer_id):
        """ this function is to check if a customer has an active reserve already
        (we only allow one at a time)
        example return data
        {'active_reserves': 0}
        if its more than 0 don't allow customer to reserve another trailer
        """
        return self._make_call('customer_active_reserves', [customer_id])

    @production_only
    def create_invoice(self, customer_id, store_id, VIN):
        """ example return data
        {'error': True, 'message': 'Error - trailer not available', 'store_id': None, 'invoice_number': None}
        {'error': False, 'message': 'Success', 'store_id': store_id, 'invoice_number': inv_no}
        """
        return self._make_call('create_invoice', [customer_id, store_id, VIN])

    def create_in_db(self, invoice_uuid):
        invoice = self.invoice_from_link(link_id=invoice_uuid)
        vin = invoice['VIN']
        try:
            email = invoice['customer_data'][0]['email_address']
        except KeyError:
            email = f"{invoice['InvoiceNumber']}@trailerplus-customer.com"
        try:
            trailer = Trailer.objects.get(vin=vin)
        except Trailer.DoesNotExist:
            invoice = TestInvoice.objects.create(
                invoice_id=invoice['InvoiceNumber'],
                customer_email=email,
                date=dt.datetime.now()
            )
            return invoice
        
        invoice = TestInvoice.objects.create(
            invoice_id=invoice['InvoiceNumber'],
            trailer=trailer,
            customer_email=email,
            date=dt.datetime.now()
        )
        return invoice

    def invoice_data(self, store_id, invoice_number):
        """example return data
        ***PLEASE DO NOT DISPLAY THE NOTE FIELDS TO THE CUSTOMER***

        {
            'CashPriceInvoice': 0,
            'Collected': Decimal('0.00'),
            'CompleteDate': None,
            'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
            'CustomerID': 1697723L,
            'CustomerName': u'JOHN WATSON',
            'CustomerPicture': None,
            'DiscountedTrailer': Decimal('7249.00'),
            'Due': Decimal('7249.00'),
            'EditDate': datetime.datetime(2020, 11, 10, 12, 51, 56),
            'InvoiceNumber': 32047L,
            'InvoiceValue': Decimal('7249.00'),
            'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
            'SalesPerson2Active': None,
            'SalesPerson2Email': None,
            'SalesPerson2LoginID': None,
            'SalesPerson2Name': None,
            'SalesPerson2Number': None,
            'SalesPerson2UserID': None,
            'SalesPersonActive': 0,
            'SalesPersonEmail': None,
            'SalesPersonLoginID': u'TRAILERSPLUS\\weblead',
            'SalesPersonName': u'Web Lead',
            'SalesPersonNumber': u'0',
            'SalesPersonUserID': u'weblead',
            'Status': 1,
            'StatusDescription': u'Quote',
            'StoreID': u'TRPL35',
            'VIN': None,
            'lines': [{'CompleteDate': None,
              'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'Description': u'7 x 16 Loadrunner 7K',
              'EditDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'ExtendedCost': Decimal('10509.00'),
              'InvoiceDate': None,
              'InvoiceNumber': 32047L,
              'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'PartNumber': u'ILRD716TA2',
              'QtyDelivered': Decimal('1.00'),
              'QtyOrdered': Decimal('1.00'),
              'SerialNumber': u'4RALS1623MK075899',
              'StoreID': u'TRPL35',
              'Taxable': 0,
              'UniqueID': 25301348L,
              'UnitCost': Decimal('10509.00'),
              'Units': u'EACH'},
             {'CompleteDate': None,
              'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'Description': u'Dealer Discount Pre-approved',
              'EditDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'ExtendedCost': Decimal('-3260.00'),
              'InvoiceDate': None,
              'InvoiceNumber': 32047L,
              'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'PartNumber': u'DISCOUNT',
              'QtyDelivered': Decimal('1.00'),
              'QtyOrdered': Decimal('1.00'),
              'SerialNumber': None,
              'StoreID': u'TRPL35',
              'Taxable': 0,
              'UniqueID': 25301349L,
              'UnitCost': Decimal('-3260.00'),
              'Units': u'EACH'},
             {'CompleteDate': None,
              'CreateDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'Description': u'Sale price Approved By luteyns Approved Sale Price HD Coupler Lock Required On The Lot',
              'EditDate': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'ExtendedCost': Decimal('0.00'),
              'InvoiceDate': None,
              'InvoiceNumber': 32047L,
              'LastChange': datetime.datetime(2020, 11, 10, 19, 51, 56),
              'PartNumber': u'NOTE',
              'QtyDelivered': Decimal('1.00'),
              'QtyOrdered': Decimal('1.00'),
              'SerialNumber': None,
              'StoreID': u'TRPL35',
              'Taxable': 0,
              'UniqueID': 25301350L,
              'UnitCost': Decimal('0.00'),
              'Units': u'EACH'}]
        }
        """
        return self._make_call('invoice_data', [store_id, invoice_number])

    def invoice_from_link(self, link_id):
        """link_id will come from the URL we email to the customer
        (example: https://www.trailersplus.com/invoice/1c31469f20d541d4a7847e95bcf999a6
            link_id would be 1c31469f20d541d4a7847e95bcf999a6 )
        return data will be the same as invoice_data function
            or if no invoice is found it will return
        {'error': True, 'message': "Couldn't find invoice"}
        """
        return self._make_call('invoice_from_link', [link_id])

    @production_only
    def add_reserve_to_invoice(self, store_id, invoice_number, response_code, auth_code, trans_id, messages):
        """please submit these wether they were successful or not
            i will add the messages as a note on unsuccessful ones for our salespeople to see
        NOTE: This is the "authorize only" transaction, do not capture it.
        example return data
        {'error': False, 'message': 'Success.'}
        """
        return self._make_call('add_reserve_to_invoice',
                               [store_id, invoice_number, response_code, auth_code, trans_id, messages])

    def invoice_payment_limits(self, store_id, invoice_number):
        """Use this to limit the max/minimum that an online payment can be for each invoice
        example return data:
        {'max': 0, 'min': 0}
        {'max': 1000, 'min': 250}
        """
        return self._make_call('invoice_payment_limits', [store_id, invoice_number])

    @production_only
    def add_payment_to_invoice(self, store_id, invoice_number, payment_amount, card_type, response_code,
                               auth_code, trans_id, messages):
        """Use this function to add auth & capture payments to the invoice
        example return data:
        True
        """
        return self._make_call('add_payment_to_invoice', [store_id, invoice_number, payment_amount, card_type,
                                                          response_code, auth_code, trans_id, messages])

    def available_appointment_slots(self, store_id, start, end):
        """use to get available appointment slots for store between start and end time
        format times like 2022-04-26 00:00:00
        all return times will be in the store's time zone
        example return data:
        ({'appointment_id': 688091L,
        'end': datetime.datetime(2022, 4, 27, 11, 0),
        'start': datetime.datetime(2022, 4, 27, 10, 0),
        'store_id': u'TRPL09'},
       {'appointment_id': 688087L,
        'end': datetime.datetime(2022, 4, 27, 12, 0),
        'start': datetime.datetime(2022, 4, 27, 11, 0),
        'store_id': u'TRPL09'},
       {'appointment_id': 688090L,
        'end': datetime.datetime(2022, 4, 27, 14, 30),
        'start': datetime.datetime(2022, 4, 27, 13, 30),
        'store_id': u'TRPL09'},
       {'appointment_id': 688088L,
        'end': datetime.datetime(2022, 4, 27, 15, 30),
        'start': datetime.datetime(2022, 4, 27, 14, 30),
        'store_id': u'TRPL09'},
       {'appointment_id': 688089L,
        'end': datetime.datetime(2022, 4, 27, 16, 30),
        'start': datetime.datetime(2022, 4, 27, 15, 30),
        'store_id': u'TRPL09'})
        """
        return self._make_call('available_appointment_slots', [store_id, start, end])

    def set_appointment(self, appointment_slot_id, customer_id):
        """use to set the appointment
        example return data:
        {'error': False, 'message': 'Appointment set'}
        {'error': True, 'message': 'appointment slot not found'}
        """
        return self._make_call('set_appointment', [appointment_slot_id, customer_id])

    def set_appointment_vin(self, appointment_slot_id, customer_id, VIN):
        """use to set the appointment
        example return data:
        {'error': False, 'message': 'Appointment set'}
        {'error': True, 'message': 'appointment slot not found'}
        """
        return self._make_call('set_appointment_vin', [appointment_slot_id, customer_id, VIN])

    def appointments_for_customer(self, customer_id):
        """use to get number of active valid appointments for customer
        example return data:
        {'error': False, 'appointments': [], 'total_appointments': 0, 'customer_id': 123456}
        {'appointments': [{'appointment_id': 714841L,
                   'display_string': '3:30 PM - 4:30 PM',
                   'end': datetime.datetime(2022, 6, 7, 16, 30),
                   'start': datetime.datetime(2022, 6, 7, 15, 30),
                   'store_id': u'TRPL09',
                   'type': u'Trailer'},
                  {'appointment_id': 714842L,
                   'display_string': '1:30 PM - 2:30 PM',
                   'end': datetime.datetime(2022, 6, 7, 14, 30),
                   'start': datetime.datetime(2022, 6, 7, 13, 30),
                   'store_id': u'TRPL09',
                   'type': u'Service'},],
        'customer_id': 1602019,
        'error': False,
        'total_appointments': 2}
        """
        return self._make_call('appointments_for_customer', [customer_id])

    def cancel_appointment(self, appointment_id):
        """use to cancel appointment
        example return data:
        {'error': True, 'message': 'Failed to cancel appointment'}
        {'error': False, 'message': 'Appointment Canceled'}
        """
        return self._make_call('cancel_appointment', [appointment_id])

    def available_service_appointment_slots(self, store_id, start, end):
        """use to get available appointment slots for store between start and end time
        format times like 2022-04-26 00:00:00
        all return times will be in the store's time zone
        example return data:
        ({'appointment_id': 688091L,
        'end': datetime.datetime(2022, 4, 27, 11, 0),
        'start': datetime.datetime(2022, 4, 27, 10, 0),
        'store_id': u'TRPL09'},
       {'appointment_id': 688087L,
        'end': datetime.datetime(2022, 4, 27, 12, 0),
        'start': datetime.datetime(2022, 4, 27, 11, 0),
        'store_id': u'TRPL09'},
       {'appointment_id': 688090L,
        'end': datetime.datetime(2022, 4, 27, 14, 30),
        'start': datetime.datetime(2022, 4, 27, 13, 30),
        'store_id': u'TRPL09'},
       {'appointment_id': 688088L,
        'end': datetime.datetime(2022, 4, 27, 15, 30),
        'start': datetime.datetime(2022, 4, 27, 14, 30),
        'store_id': u'TRPL09'},
       {'appointment_id': 688089L,
        'end': datetime.datetime(2022, 4, 27, 16, 30),
        'start': datetime.datetime(2022, 4, 27, 15, 30),
        'store_id': u'TRPL09'})
        """
        return self._make_call('available_service_appointment_slots', [store_id, start, end])

    def set_service_appointment(self, appointment_slot_id, customer_id, service_type):
        """use to set the appointment
        example return data:
        {'error': False, 'message': 'Appointment set'}
        {'error': True, 'message': 'appointment slot not found'}
        """
        return self._make_call('set_service_appointment', [appointment_slot_id, customer_id, service_type])


"""
Flow for trailer reserve:
1) get_or_create_customer & store the returned customer_id
2) trailer_status - to make sure trailer is still available
3) customer_active_reserves - to make sure customer doesn't already have another trailer reserved
4) create_invoice  - save store_id and invoice_number
5) do the transaction with authorize.net (authorize only transaction)
6) add_reserve_to_invoice - this will add the reserve in our system and update the status of the trailer in our system


Flow for invoice payment:
1) our agents email special links to our customers like https://www.trailersplus.com/invoice/1c31469f20d541d4a7847e95bcf999a6
2) invoice_from_link - get store_id and invoice_number
3) invoice_data - pull to display to customer
4) invoice_payment_limits - to get min/max the customer can pay (can be 0 for invoices that have already had a payment applied)
5) do the transaction with authorize.net (auth & capture type transaction)
6) add_payment_to_invoice - submit result from #5
"""
