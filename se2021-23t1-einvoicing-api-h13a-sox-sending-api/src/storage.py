"""
Storage
Filename: storage.py

Author: Jacqueline
Created: 06/04/2023

Description: Allows user to upload invoices, list invoices, retrieve invoices,
delete invoices from their personal storage. It also allows users to undelete
invoices that they may have accidentally deleted.
"""
import datetime
from data_base import data_base
from error import InputError, AccessError

def upload_invoice(user_id, data):
    store = data_base.get()
    invoices = store['invoices']
    users = store['users']

    # Error checking
    if user_id not in users.keys():
        raise AccessError("Invalid user_id")

    # Add invoice
    invoice_id = len(invoices.keys())
    now = datetime.datetime.now()
    date = now.strftime("%m/%d/%Y, %H:%M:%S")
    invoices[invoice_id] = {'invoice_id' : invoice_id , 'owner': user_id, 'created_date': date, 'data': data, 'deleted': False}
    data_base.set(store)

    return { 'invoice_id': invoice_id }

def list_invoices(user_id):
    store = data_base.get()
    invoices = store['invoices']
    users = store['users']

    # Error Checking
    if user_id not in users.keys():
        raise AccessError("user_id not in users")

    # List of invoices owned by user and NOT deleted
    user_invoices = [invoice for invoice in invoices.values() if invoice['owner'] == user_id and invoice['deleted'] == False]
    return { 'invoices': user_invoices }

def retrieve_invoice(user_id, invoice_id):
    store = data_base.get()
    invoices = store['invoices']
    users = store['users']

    # Error Checking
    if user_id not in users.keys():
        raise AccessError("Invalid user_id")
    if invoice_id not in invoices.keys():
        raise InputError("Invalid invoice_id")
    invoice = invoices[invoice_id]
    if invoice['owner'] != user_id:
        raise AccessError("User does not have access to this invoice")
    if invoice['deleted']:
        raise InputError("Invoice has been deleted")

    return { 'invoice': invoice }

def delete_invoice(user_id, invoice_id):
    store = data_base.get()
    invoices = store['invoices']
    users = store['users']

    # Error Checking
    if user_id not in users.keys():
        raise AccessError("Invalid user_id")
    if invoice_id not in invoices.keys():
        raise InputError("Invalid invoice_id")
    invoice = invoices[invoice_id]
    if invoice['owner'] != user_id:
        raise AccessError("User does not have access to this invoice")
    if invoice['deleted']:
        raise InputError("Invoice has been deleted")

    # Delete Invoice
    invoice['deleted'] = True
    invoices[invoice_id] = invoice
    store['invoices'] = invoices
    data_base.set(store)
    return {}

def undelete_invoice(user_id, invoice_id):
    store = data_base.get()
    invoices = store['invoices']
    users = store['users']

    # Error Checking
    if user_id not in users.keys():
        raise AccessError("Invalid user_id")
    if invoice_id not in invoices.keys():
        raise InputError("Invalid invoice_id")
    invoice = invoices[invoice_id]
    if invoice['owner'] != user_id:
        raise AccessError("User does not have access to this invoice")
    if not invoice['deleted']:
        raise InputError("Invoice is not deleted")

    # Un Delete Invoice
    invoice['deleted'] = False
    invoices[invoice_id] = invoice
    store['invoices'] = invoices
    data_base.set(store)
    return {}
