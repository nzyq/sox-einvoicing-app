# Tests for sending an invoice
from src.send_invoice import send_invoice

# Successful email sending -> Report1
def test_send_successful_invoice():
    request_data = send_invoice("seng2021sox@gmail.com", "soxreceiver@gmail.com", 'fxijpajcmsdzocql', "tests/example2.xml")
    communication_report = request_data['communication_report']
    assert (communication_report['sender'] == "seng2021sox@gmail.com")
    assert (communication_report['recipient'] == "soxreceiver@gmail.com")
    assert (communication_report['status'] == "Successful")

# Unsuccessful email sending -> Report
def test_send_incorrect_invoice():
    request_data = send_invoice("wrongemail@gmail.com", "soxreceiver@gmail.com", 'i<3seng2021', "tests/example1.xml")
    print(request_data)
    communication_report = request_data['communication_report']
    assert (communication_report['sender'] == "wrongemail@gmail.com")
    assert (communication_report['recipient'] == "soxreceiver@gmail.com")
    assert (communication_report['status'] == "Unsuccessful")
