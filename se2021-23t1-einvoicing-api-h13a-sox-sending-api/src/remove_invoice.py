"""
Remove Invoice
Filename: remove_invoice.py

Author: Ahmad, Jacqueline
Created: 11/03/2023

Description: Removes an invoice from a targeted email
"""
from data_base import data_base


def remove_invoice(email_id, filename):
    store = data_base.get()
    emails = store['emails']
    msg = emails[email_id]
    # Data base
    for item in msg.get_payload():
        if item.get_filename() == filename:
            msg.get_payload().remove(item)
    # Store back into data base
    emails[email_id] = msg
    store['emails'] = emails
    data_base.set(store)
