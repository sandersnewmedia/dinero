import os
import uuid
import dinero
from dinero.exceptions import *

## These tests require that you provide settings for authorize.net and set up
## your account to reject invalid CVV and AVS responses
try:
    import authorize_net_configuration
except ImportError:
    LOGIN_ID = os.environ["AUTHNET_LOGIN_ID"]
    TRANSACTION_KEY = os.environ["AUTHNET_TRANSACTION_KEY"]
    dinero.configure({
        'authorize.net': {
            'type': 'dinero.gateways.AuthorizeNet',
            'login_id': LOGIN_ID,
            'transaction_key': TRANSACTION_KEY,
            'default': True,
        }
    })


## For information on how to trigger specific errors, see http://community.developer.authorize.net/t5/Integration-and-Testing/Triggering-Specific-Transaction-Responses-Using-Test-Account/td-p/4361


def test_create_customer_no_email_error():
    options = {
    }

    try:
        customer = dinero.Customer.create(gateway_name='authorize.net', **options)
        customer.delete()
        assert False, "InvalidCustomerException should be raised"
    except InvalidCustomerException:
        pass


def test_create_customer_not_enough_payment_info_error():
    options = {
        'email': '{0}@example.com'.format(uuid.uuid4()),
        'number': '4' + '1' * 14
    }

    try:
        customer = dinero.Customer.create(gateway_name='authorize.net', **options)
        customer.delete()
        assert False
    except InvalidCardError:
        pass
