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


# Successful upload of invoice
def test_upload_invoice(clear, create_user):
    request_data = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"})
    invoice_id = request_data.json()['invoice_id']
    status = request_data.status_code
    assert (invoice_id == 0)
    assert (status == 200)


# Multiple invoices
def test_multiple_invoices(clear, create_user):
    request_data_1 = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice"})
    invoice_id_1 = request_data_1.json()['invoice_id']
    status_1 = request_data_1.status_code
    request_data_2 = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': create_user, 'data': "Data for Invoice 2"})
    invoice_id_2 = request_data_2.json()['invoice_id']
    status_2 = request_data_2.status_code
    assert (invoice_id_1 == 0)
    assert (invoice_id_2 == 1)
    assert (status_1 == 200)
    assert (status_2 == 200)


# Invalid user id
def test_invalid_user_id(clear):
    request_data = requests.post(other.UPLOAD_INVOICE_URL, json={'user_id': 2, 'data': "Data for Invoice"})
    status = request_data.status_code
    assert (status == 403) # Access error


