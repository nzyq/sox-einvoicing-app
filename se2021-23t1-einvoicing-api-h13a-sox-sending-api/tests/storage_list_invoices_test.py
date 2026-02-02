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


# Successful list of invoice
def test_list_invoice(clear, create_user):
    requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"})
    request_data = requests.get(other.LIST_INVOICES_URL, params={'user_id': create_user})
    invoices = request_data.json()['invoices']
    status = request_data.status_code
    assert (len(invoices) == 1)
    assert (status == 200)


# Multiple invoices listed
def test_multiple_invoices(clear, create_user):
    requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"})
    requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice 2"})
    requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice 3"})
    request_data = requests.get(other.LIST_INVOICES_URL, params={'user_id': create_user})
    invoices = request_data.json()['invoices']
    status = request_data.status_code
    assert (len(invoices) == 3)
    assert (status == 200)


# Empty invoice list
def test_empty_list(clear, create_user):
    request_data = requests.get(other.LIST_INVOICES_URL, params={'user_id': create_user})
    invoices = request_data.json()['invoices']
    status = request_data.status_code
    assert (len(invoices) == 0)
    assert (status == 200)


# Invalid user id
def test_invalid_user_id(clear):
    request_data = requests.get(other.LIST_INVOICES_URL, params={'user_id': 2})
    status = request_data.status_code
    assert (status == 403) # Access error

