# Tests for creating an email
from src.create_email import create_email
from src.send_invoice import send_email

# Successful email creation -> email_id is returned
def test_create_email_1():
    request_data = create_email("seng2021sox@gmail.com", "soxreceiver@gmail.com", "E-Invoice Subject", "E-Invoice Content!")
    email_id = request_data["email_id"]
    assert (email_id == 0) # First Email
    # Send email
    request_data_2 = send_email(email_id, 'fxijpajcmsdzocql')
    report_id = request_data_2["report_id"]
    assert (report_id == 0) # First report


# Multiple email created
def test_create_email_2():
    request_data = create_email("seng2021sox@gmail.com", "soxreceiver@gmail.com", "E-Invoice Subject 2", "E-Invoice Content! 2")
    email_id = request_data["email_id"]
    assert (email_id == 1) # Second report
    # Send email
    request_data_2 = send_email(email_id, 'fxijpajcmsdzocql')
    report_id = request_data_2["report_id"]
    assert (report_id == 1) # Second report
