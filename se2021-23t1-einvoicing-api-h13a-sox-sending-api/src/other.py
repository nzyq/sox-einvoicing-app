"""
Other
Filename: other.py

Author: Jacqueline
Created: 10/03/2023

Description: Contains the URLs of the API routes
and contains a clear function that empties the database
"""

import hashlib
import secrets
import jwt
import re
from config import url
from data_base import data_base


SEND_INVOICE_URL = f"{url}/send/send_invoice"
ATTACH_INVOICE_URL = f"{url}/send/attach_invoice"
CREATE_EMAIL_URL = f"{url}/send/create_email"
CLEAR_URL = f"{url}/send/clear"
LOGIN_URL = f"{url}/auth/login"
LOGOUT_URL = f"{url}/auth/logout"
REGISTER_URL = f"{url}/auth/register"
AUTH_PASSWORDRESET_REQUEST_URL = f"{url}/auth/passwordreset/request"
AUTH_PASSWORDRESET_RESET_URL = f"{url}/auth/passwordreset/reset"
UPLOAD_INVOICE_URL = f"{url}/storage/upload"
LIST_INVOICES_URL = f"{url}/storage/list"
RETRIEVE_INVOICE_URL = f"{url}/storage/retrieve_invoice"
DELETE_INVOICE_URL = f"{url}/storage/delete_invoice"
UNDELETE_INVOICE_URL = f"{url}/storage/undelete_invoice"
JWT_SECRET = "SENG2021_SOX"


# This function clears the data base environment for each test
def clear():
    store = data_base.get()
    store['communication_reports'] = {}
    store['emails'] = {}
    store['users'] = {}
    store['reset_codes'] = {}
    store['invoices'] = {}
    data_base.set(store)


def verify_user(auth_user_id: int)->bool:
    users = data_base.get()['users']
    return bool(auth_user_id in users.keys())


def user_id_from_JWT(token: str)->int:
    jwt_payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    return int(jwt_payload['auth_user_id'])


def is_valid_email(email: str)->bool:
    return bool(re.search(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email))


def is_email_taken(email: str)->bool:
    store = data_base.get()
    users = store['users']
    for user in users.values():
        if user['email'] == email:
            return True
    return False


def id_from_email(email: str)->int:
    store = data_base.get()
    users = store['users']
    for id, user in users.items():
        if user['email'] == email:
            return int(id)
    return None


def is_valid_JWT(jwt_string: str)->bool:
    try:
        jwt_payload = jwt.decode(jwt_string, JWT_SECRET, algorithms=['HS256'])
    except:
        return False
    store = data_base.get()
    users = store['users']
    if not verify_user(jwt_payload['auth_user_id']):
        return False
    if jwt_payload['user_session_id'] not in users[jwt_payload['auth_user_id']]['sessions']:
        return False
    return True


def create_JWT(auth_user_id: int)->str:
    store = data_base.get()
    new_session = len(store['users'][auth_user_id]['sessions'])
    store['users'][auth_user_id]['sessions'].append(new_session)
    payload = {'auth_user_id': auth_user_id, 'user_session_id': new_session}
    data_base.set(store)
    new_jwt = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return new_jwt


def generate_reset_code(email: str)->int:
    payload = email + str(secrets.randbits(128))
    hash = hashlib.sha256(payload.encode()).hexdigest()
    return int(hash[0:6], 16)
