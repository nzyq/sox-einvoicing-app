"""
Send Invoice
Filename: send_invoice.py

Author: Vansh, James, Jacqueline
Created: 11/03/2023

Description: Allows the user to send in invoice
via email
"""

import smtplib
from multipledispatch import dispatch
from data_base import data_base
from create_email import create_email
from attach_invoice import attach_invoice
from generate_report import generate_report
from storage import retrieve_invoice
from error import InputError


def send_email(email_id, user_pass):
    store = data_base.get()
    emails = store['emails']
    email_item = emails[email_id]

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        # Login error
        try:
            server.login(email_item['From'], user_pass)
        except smtplib.SMTPAuthenticationError:
            report_id = generate_report(email_item['From'], email_item['To'],
                                        email_item["Subject"], {400: "Input Error"})
            return {"report_id": report_id}
        errors = server.sendmail(
            email_item['From'], email_item['To'], email_item.as_string())
    report_id = generate_report(
        email_item['From'], email_item['To'], email_item["Subject"], errors)
    return {"report_id": report_id}


# Quick function with default subject and content
@dispatch(str, str, str, str, str)
def send_invoice(sender_email, receiver_email, user_pass, file_name, xml_data) -> dict:
    email_id = create_email(sender_email, receiver_email,
                            "E-Invoice", "Thankyou for your purchase!")['email_id']
    attach_invoice(email_id, file_name, xml_data)
    report_id = send_email(email_id, user_pass)["report_id"]

    # Retrieve report and return it
    store = data_base.get()
    reports = store['communication_reports']
    report = reports[report_id]
    return {'communication_report': report}


@dispatch(int, str, str, str, int)
def send_invoice(user_id, receiver_email, user_pass, file_name, invoice_id) -> dict:
    store = data_base.get()
    users = store['users']
    sender_email = users['email']
    invoice = retrieve_invoice(invoice_id)
    xml_data = invoice['data']
    return send_invoice(sender_email, receiver_email, user_pass, file_name, xml_data)
