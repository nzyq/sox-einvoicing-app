from authentication import auth_register, auth_login
from storage import upload_invoice
from send_invoice import send_invoice

if __name__ == '__main__':
    user_id = auth_register("seng2021sox@gmail.com", "password!", "Jacqueline", "Chen")['auth_user_id']
    auth_login("seng2021sox@gmail.com", "password!")
    invoice_id = upload_invoice(user_id, "E-Invoice Rulez")['invoice_id']
    result = send_invoice(user_id, "soxreceiver@gmail.com", 'fxijpajcmsdzocql', "Invoice", invoice_id)
    print(result)

