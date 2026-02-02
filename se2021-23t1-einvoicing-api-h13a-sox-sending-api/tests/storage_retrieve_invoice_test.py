# Tests for sending an invoice
from src.config import port, url
from src import other
import requests
import pytest
import tempfile


@pytest.fixture
def clear():
    requests.delete(other.CLEAR_URL, json={})


@pytest.fixture
def create_user():
    response = requests.post(other.REGISTER_URL, json={"email":"seng2021sox@gmail.com", "password":"passwordlong", "name_first":"SOX", "name_last":"Account"})
    return response.json()['auth_user_id']

@pytest.fixture
def create_user_2():
    response = requests.post(other.REGISTER_URL, json={"email":"soxreceiver@gmail.com", "password":"passwordlong", "name_first":"SOX", "name_last":"Receiver"})
    return response.json()['auth_user_id']


# Successful Retrieval of Invoice
def test_retrieve_invoice(clear, create_user):
    invoice_id = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"}).json()['invoice_id']
    request_data = requests.get(other.RETRIEVE_INVOICE_URL, params={'user_id': create_user, 'invoice_id': invoice_id})
    invoice = request_data.json()['invoice']
    status = request_data.status_code
    assert (invoice['owner'] == create_user)
    assert (invoice['data'] == "Data for Invoice")
    assert (status == 200)


# Successful Retrieval from multiple invoices
def test_retrieve_invoice_multiple_invoices(clear, create_user):
    requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"})
    requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice 2"})
    invoice_id = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice 3"}).json()['invoice_id']
    request_data = requests.get(other.RETRIEVE_INVOICE_URL, params={'user_id': create_user, 'invoice_id': invoice_id})
    invoice = request_data.json()['invoice']
    status = request_data.status_code
    assert (invoice['owner'] == create_user)
    assert (invoice['data'] == "Data for Invoice 3")
    assert (status == 200)


# Invalid user id
def test_invalid_user_id(clear, create_user):
    invoice_id = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"}).json()['invoice_id']
    request_data = requests.get(other.RETRIEVE_INVOICE_URL, params={'user_id': 2, 'invoice_id': invoice_id})
    status = request_data.status_code
    assert (status == 403) # Access error


# Invalid invoice id
def test_invalid_invoice_id(clear, create_user):
    request_data = requests.get(other.RETRIEVE_INVOICE_URL, params={'user_id': create_user, 'invoice_id': 2})
    status = request_data.status_code
    assert (status == 400) # Input error


# User does not have access to invoice
def test_user_no_access(clear, create_user, create_user_2):
    invoice_id = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"}).json()['invoice_id']
    request_data = requests.get(other.RETRIEVE_INVOICE_URL, params={'user_id': create_user_2, 'invoice_id': invoice_id})
    status = request_data.status_code
    assert (status == 403) # Access error


# Invoice already deleted
def test_invoice_deleted(clear, create_user):
    invoice_id = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice 3"}).json()['invoice_id']
    requests.delete(other.DELETE_INVOICE_URL, json={'user_id': create_user, 'invoice_id': invoice_id})
    request_data = requests.get(other.RETRIEVE_INVOICE_URL, params={'user_id': create_user, 'invoice_id': invoice_id})
    status = request_data.status_code
    assert (status == 400) # Input error
