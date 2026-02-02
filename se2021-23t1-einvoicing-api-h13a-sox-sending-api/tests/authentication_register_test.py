import pytest
import requests
from src.config import url
import src.other as other

@pytest.fixture
def clear_store():
    requests.delete(other.CLEAR_URL, json={})

def test_user_registration(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    assert response.status_code == 200
    assert (response.json()['auth_user_id'] == 0)

def test_auth_register_multiple_users(clear_store):
    response_0 = requests.post(other.REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"abcdefghi", "name_last":"jklmnopqrst"})
    response_1 = requests.post(other.REGISTER_URL, json={"email":"z55556@unsw.edu.au", "password":"passwordlong", "name_first":" **(&(abcdefghi__  ", "name_last":"jklmnopqrst&**uv"})
    response_2 = requests.post(other.REGISTER_URL, json={"email":"z55557@unsw.edu.au", "password":"passwordlong", "name_first":"ABCDEFGHI", "name_last":"JKLMNOPQRSTUVWXYZ"})
    id_0 = response_0.json()['auth_user_id']
    id_1 = response_1.json()['auth_user_id']
    id_2 = response_2.json()['auth_user_id']
    assert (response_0.status_code == 200)
    assert (response_1.status_code == 200)
    assert (response_2.status_code == 200)
    assert (id_0 == 0)
    assert (id_1 == 1)
    assert (id_2 == 2)

def test_error_email_not_valid(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"tsgyd", "password":"34rd^hds)", "name_first": "Johnny", "name_last":"Smith"})
    assert response.status_code == 400

def test_error_password_short(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"pa33", "name_first":"Marc", "name_last":"Chee"})
    assert response.status_code == 400

def test_error_email_used(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"thi3isn0t@pa33wor&", "name_first":"Steve", "name_last":"Jobs"})
    assert response.status_code == 200
    response2 = requests.post(other.REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"newpassword", "name_first":"Steve", "name_last":"Wozniak"})
    assert response2.status_code == 400

def test_error_first_name_short(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"longpassword", "name_first":"", "name_last":"Li"})
    assert response.status_code == 400

def test_error_first_name_long(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"longpassword", "name_first":"THISISIAREALLYALONGNAMEWHICHISOUTOFBOUNDSDEFINITIELY", "name_last":"Li"})
    assert response.status_code == 400

def test_error_last_name_short(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"goodpass", "name_first":"Simon", "name_last":""})
    assert response.status_code == 400

def test_error_last_name_long(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"z123456789@unsw.edu.au", "password":"goodpass", "name_first":"Simon", "name_last":"THISISIAREALLYALONGNAMEWHICHISOUTOFBOUNDSDEFINITIELY"})
    assert response.status_code == 400
