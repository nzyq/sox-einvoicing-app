# Tests for sending an invoice
from src.config import port, url
from src import other
import requests
import pytest
import tempfile


@pytest.fixture
def clear():
    requests.delete(other.CLEAR_URL, json={})


# Successful email creation -> email_id is returned
def test_create_email(clear):
    request_data = requests.post(other.CREATE_EMAIL_URL, json={'receiver_email': "soxreceiver@gmail.com",
                                                               'subject': 'E-Invoice Subject', 'content': 'E-Invoice Content!'})
    email_id = request_data.json()['email_id']
    status = request_data.status_code
    assert (email_id == 0)
    assert (status == 200)


# Multiple emails created -> email_id increments
def test_send_unsuccessful_invoice(clear):
    request_data_1 = requests.post(other.CREATE_EMAIL_URL, json={'receiver_email': "soxreceiver@gmail.com",
                                                               'subject': 'E-Invoice Subject', 'content': 'E-Invoice Content!'})
    email_id_1 = request_data_1.json()['email_id']
    status_1 = request_data_1.status_code
    request_data_2 = requests.post(other.CREATE_EMAIL_URL, json={'receiver_email': "soxreceiver@gmail.com",
                                                               'subject': 'E-Invoice Subject 2', 'content': 'E-Invoice Content! 2'})
    email_id_2 = request_data_2.json()['email_id']
    status_2 = request_data_2.status_code
    assert (email_id_1 == 0)
    assert (email_id_2 == 1)
    assert (status_1 == 200)
    assert (status_2 == 200)
