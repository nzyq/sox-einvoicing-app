# Tests for sending an invoice
from src.authentication import auth_login, auth_logout, auth_register, password_reset_request, reset_user_password

def test_register_login_logout():
    register_request = auth_register("soxreceiver@gmail.com", "passwordlong", "Jake", "Renzella")
    assert (register_request["auth_user_id"] == 0)

    login_request = auth_login("soxreceiver@gmail.com", "passwordlong")
    assert (login_request["auth_user_id"] == 0)
    token = login_request["token"]
    logout_request = auth_logout(token)
    assert (logout_request == {})

def test_password_request():
    reset_request = password_reset_request("soxreceiver@gmail.com")
    communication_report = reset_request['communication_report']
    print(communication_report)
    assert (communication_report['sender'] == "seng2021sox@gmail.com")
    assert (communication_report['recipient'] == "soxreceiver@gmail.com")
    assert (communication_report['status'] == "Successful")
