# Tests for adding an invoice to an email
from src.config import port, url
from src import other
import requests
import pytest

@pytest.fixture
def clear():
    requests.delete(other.CLEAR_URL, json={})


@pytest.fixture
def create_email():
    request_data = requests.post(other.CREATE_EMAIL_URL, json={'receiver_email': "soxreceiver@gmail.com",
                                                               'subject': 'E-Invoice Subject', 'content': 'E-Invoice Content!'})
    email_id = request_data.json()['email_id']
    return email_id


# Add invoice -> Returns an invoice_id for the invoice
def test_add_invoice(clear, create_email):
    request_data = requests.put(other.ATTACH_INVOICE_URL, json={'email_id': 0, 'filename': "invoice.xml", 'xml_data': "Invoice for purchasing 20 eggs"})

    # Can check if there is attachment in email but whitebox since we should not know how the emails are stored
    print(request_data)
    status = request_data.status_code
    assert (status == 200) # Success

# Add multiple invoices -> Invoice_id should increment
def test_add_multiple_invoices(clear, create_email):
    request_data_1 = requests.put(other.ATTACH_INVOICE_URL, json={'email_id': create_email, 'filename': "invoice.xml", 'xml_data': "Invoice for purchasing 20 eggs"})
    request_data_2 = requests.put(other.ATTACH_INVOICE_URL, json={'email_id': create_email, 'filename': "invoice1.xml", 'xml_data': "Invoice for purchasing 30 eggs"})
    request_data_3 = requests.put(other.ATTACH_INVOICE_URL, json={'email_id': create_email, 'filename': "invoice2.xml", 'xml_data': "Invoice for purchasing 40 eggs"})
    status_1 = request_data_1.status_code
    status_2 = request_data_2.status_code
    status_3 = request_data_3.status_code
    assert (status_1 == 200) # Success
    assert (status_2 == 200) # Success
    assert (status_3 == 200) # Success

# Add non-valid email_id -> Error message
def test_non_valid_email(clear):
    request_data = requests.put(other.ATTACH_INVOICE_URL, json = {'email_id': 0, 'filename': "invoice.xml", 'xml_data': "Invoice for purchasing 20 eggs"})
    status = request_data.status_code
    assert (status == 400) # Input error
