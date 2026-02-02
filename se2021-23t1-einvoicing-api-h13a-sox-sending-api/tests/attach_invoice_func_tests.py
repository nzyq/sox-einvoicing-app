# Tests for adding an invoice to an email
from src.config import port, url
from src.create_email import create_email
from src.attach_invoice import attach_invoice
from src import other
import requests
import pytest
import tempfile



# Add invoice -> Returns an invoice_id for the invoice
def test_add_invoice():
    create_email("seng2021sox@gmail.com", "soxreceiver@gmail.com", "E-Invoice Subject 2", "E-Invoice Content! 2")
    request_data = attach_invoice(0, "invoice.xml", "Invoice for purchasing 20 eggs")

    # Can check if there is attachment in email but whitebox since we should not know how the emails are stored
    print(request_data)
    assert request_data == {}

# Add multiple invoices -> Invoice_id should increment
def test_add_multiple_invoices():
    create_email("seng2021sox@gmail.com", "soxreceiver@gmail.com", "E-Invoice Subject 2", "E-Invoice Content! 2")
    request_data = attach_invoice(0, "invoice.xml", "Invoice for purchasing 20 eggs")
    request_data = attach_invoice(0, "invoice1.xml", "Invoice for purchasing 30 eggs")
    request_data = attach_invoice(0, "invoice2.xml", "Invoice for purchasing 40 eggs")

    # Can check if there is attachment in email but whitebox since we should not know how the emails are stored
    print(request_data)
    assert request_data == {}
