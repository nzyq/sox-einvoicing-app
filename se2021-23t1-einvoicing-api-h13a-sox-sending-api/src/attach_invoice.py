"""
Attach Invoice
Filename: attach_invoice.py

Author: Ahmad, Jacqueline
Created: 11/03/2023

Description: Allows the user to attach an invoice to an email
"""

from email.mime.base import MIMEBase
from email import encoders
from data_base import data_base
from error import InputError
from os import path


def attach_invoice(email_id, file_name, xml_data):
    store = data_base.get()
    emails = store['emails']

    # Error checking
    if (email_id not in emails.keys()):
        raise InputError(description="Invalid email_id")

    msg = emails[email_id]

    # Add the UBL XML invoice as an attachment
    part = MIMEBase('application', "octet-stream")
    part.set_payload(xml_data)
    encoders.encode_base64(part)
    # or whatever you want to call it
    part.add_header('Content-Disposition', 'attachment',
                    filename=file_name)   # should put the invoice_ID here later
    msg.attach(part)

    emails[email_id] = msg
    store['emails'] = emails
    data_base.set(store)  # Store email

    return {}
