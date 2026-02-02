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


# Successful Un-Deletion of Invoice
def test_undelete_invoice(clear, create_user):
    invoice_id = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"}).json()['invoice_id']
    assert (invoice_id == 0)
    requests.delete(other.DELETE_INVOICE_URL, json={'user_id': create_user, 'invoice_id': invoice_id})
    user_invoices = requests.get(other.LIST_INVOICES_URL, params={'user_id': create_user}).json()['invoices']
    assert (len(user_invoices) == 0) # deleted
    request_data = requests.put(other.UNDELETE_INVOICE_URL, json={'user_id': create_user, 'invoice_id': invoice_id})
    user_invoices = requests.get(other.LIST_INVOICES_URL, params={'user_id': create_user}).json()['invoices']
    status = request_data.status_code
    assert (request_data.json() == {})
    assert (len(user_invoices) == 1) # un deleted
    assert (status == 200)


# Invalid user id
def test_invalid_user_id(clear, create_user):
    invoice_id = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"}).json()['invoice_id']
    request_data = requests.put(other.UNDELETE_INVOICE_URL, json={'user_id': 2, 'invoice_id': invoice_id})
    status = request_data.status_code
    assert (status == 403) # Access error


# Invalid invoice id
def test_invalid_invoice_id(clear, create_user):
    request_data = requests.put(other.UNDELETE_INVOICE_URL, json={'user_id': create_user, 'invoice_id': 2})
    status = request_data.status_code
    assert (status == 400) # Input error


# User does not have access to invoice
def test_user_no_access(clear, create_user, create_user_2):
    invoice_id = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"}).json()['invoice_id']
    requests.delete(other.DELETE_INVOICE_URL, json={'user_id': create_user, 'invoice_id': invoice_id})
    request_data = requests.put(other.UNDELETE_INVOICE_URL, json={'user_id': create_user_2, 'invoice_id': invoice_id})
    status = request_data.status_code
    assert (status == 403) # Access error


# Invoice not deleted
def test_invoice_not_deleted(clear, create_user):
    invoice_id = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice 3"}).json()['invoice_id']
    request_data = requests.put(other.UNDELETE_INVOICE_URL, json={'user_id': create_user, 'invoice_id': invoice_id})
    status = request_data.status_code
    assert (status == 400) # Input error