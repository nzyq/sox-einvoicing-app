"""
Application
Filename: application.py

Author: Jacqueline, Ahmad
Created: 11/03/2023

Description: Contains the server information for
the API routes and swagger API methods
"""

import signal
import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
#import config
from send_invoice import send_invoice, send_email
from attach_invoice import attach_invoice
from create_email import create_email
from other import clear
from authentication import auth_login, auth_logout, auth_register, password_reset_request, reset_user_password
from storage import upload_invoice, list_invoices, retrieve_invoice, delete_invoice, undelete_invoice

def quit_gracefully(*args):
    sys.exit()


def default_handler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


application = Flask(__name__, static_folder="../static", static_url_path='/static/')

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
# Our API url (can of course be a local resource)
API_URL = 'http://127.0.0.1:9090/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config.
    #    See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

application.register_blueprint(swaggerui_blueprint)

CORS(application)

application.config['TRAP_HTTP_EXCEPTIONS'] = True
application.register_error_handler(Exception, default_handler)


# API Routes
@application.route('/static/<path:path>')
def serve_static_path(path):
    return send_from_directory('', path)


@application.route("/swagger.yaml", methods=['GET'])
def serve_swagger():
    return send_from_directory('static', 'swagger.yaml')


@application.route("/send/clear", methods=['DELETE'])
def handle_clear():
    clear()
    return {}


@application.route("/auth/register", methods=['POST'])
def handle_register():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    name_first = request_data['name_first']
    name_last = request_data['name_last']
    return auth_register(email, password, name_first, name_last)


@application.route("/auth/login", methods=['POST'])
def handle_login():
    request_data = request.get_json()
    email = request_data['email']
    password = request_data['password']
    return auth_login(email, password)


@application.route("/auth/logout", methods=['POST'])
def handle_logout():
    request_data = request.get_json()
    token = request_data['token']
    return auth_logout(token)


@application.route("/auth/passwordreset/request", methods=['POST'])
def handle_reset_request():
    request_data = request.get_json()
    email = request_data['email']
    return password_reset_request(email)


@application.route("/auth/passwordreset/reset", methods=['POST'])
def handle_reset():
    request_data = request.get_json()
    reset_code = str(request_data['reset_code'])
    new_password = str(request_data['new_password'])
    return reset_user_password(reset_code, new_password)


@application.route("/send/send_invoice", methods=['POST'])
def handle_send_invoice():
    request_data = request.get_json()
    receiver_email = request_data['receiver_email']
    file_name = request_data['filename']
    xml_data = request_data['xml_data']
    return send_invoice("einvoice.solution@gmail.com", receiver_email, "bzqgzvbschotmywj", file_name, xml_data)


@application.route("/send/create_email", methods=['POST'])
def handle_create_email():
    request_data = request.get_json()
    receiver_email = request_data['receiver_email']
    subject = request_data['subject']
    content = request_data['content']

    return create_email("einvoice.solution@gmail.com", receiver_email, subject, content)


@application.route("/send/attach_invoice", methods=['PUT'])
def handle_attach_invoice():
    request_data = request.get_json()
    email_id = int(request_data['email_id'])
    file_name = request_data['filename']
    xml_data = request_data['xml_data']
    return attach_invoice(email_id, file_name, xml_data)


@application.route("/send/send_email", methods=['POST'])
def handle_send_email():
    request_data = request.get_json()
    email_id = int(request_data['email_id'])
    return send_email(email_id, "bzqgzvbschotmywj")


@application.route("/storage/upload", methods=['POST'])
def handle_upload_invoice():
    request_data = request.get_json()
    user_id = int(request_data['user_id'])
    data = request_data['data']
    return upload_invoice(user_id, data)


@application.route("/storage/list", methods=['GET'])
def handle_list_invoices():
    request_data = request.get_json()
    user_id = int(request_data['user_id'])
    return list_invoices(user_id)


@application.route("/storage/retrieve_invoice", methods=['GET'])
def handle_retrieve_invoice():
    request_data = request.get_json()
    user_id = int(request_data['user_id'])
    invoice_id = int(request_data['invoice_id'])
    return retrieve_invoice(user_id, invoice_id)


@application.route("/storage/delete_invoice", methods=['DELETE'])
def handle_delete_invoice():
    request_data = request.get_json()
    user_id = int(request_data['user_id'])
    invoice_id = int(request_data['invoice_id'])
    return delete_invoice(user_id, invoice_id)


@application.route("/storage/undelete_invoice", methods=['PUT'])
def handle_undelete_invoice():
    request_data = request.get_json()
    user_id = int(request_data['user_id'])
    invoice_id = int(request_data['invoice_id'])
    return undelete_invoice(user_id, invoice_id)


# To run the API server
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)
    application.run()
