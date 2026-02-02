# Tests for sending an invoice
from src.config import port, url
from src import other
import requests
import pytest
import tempfile


@pytest.fixture
def clear():
    requests.delete(other.CLEAR_URL, json={})


# Successful email sending -> Report says "Successful"
def test_send_successful_invoice(clear):
    request_data = requests.post(other.SEND_INVOICE_URL, json={'receiver_email': "soxreceiver@gmail.com", 'filename': "invoice.xml", 'xml_data': "Invoice for purchasing 20 eggs"})
    communication_report = request_data.json()['communication_report']
    status = request_data.status_code
    assert (communication_report['sender'] == "einvoice.solution@gmail.com")
    assert (communication_report['recipient'] == "soxreceiver@gmail.com")
    assert (communication_report['status'] == "Successful")
    assert (status == 200)