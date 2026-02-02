"""
Delete email
Filename: delete_email.py

Author: Vansh, Jacqueline
Created: 11/03/2023

Description: Deletes an email from the database
"""
from data_base import data_base

def delete_email(email_id: int) -> None:
    store = data_base.get()
    emails = store['emails']
    del emails[email_id]
    store['emails'] = emails
    data_base.set(store)
