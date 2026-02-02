import pytest
import requests
from src.config import url
import src.other as other

@pytest.fixture
def clear_store():
    requests.delete(other.CLEAR_URL, json={})

TEST_USER_EMAIL = "seng2021sox@gmail.com"

@pytest.fixture
def create_user():
    user_input = {'email': TEST_USER_EMAIL,
                  'password': "badpassword123", 'name_first': "Ji", 'name_last': "Sun"}
    request_data = requests.post(other.REGISTER_URL, json=user_input)
    user_info = request_data.json()
    return user_info

def test_request_user_exists(clear_store, create_user):
    reset_request = requests.post(other.AUTH_PASSWORDRESET_REQUEST_URL, json={"email": TEST_USER_EMAIL})
    assert reset_request.status_code == 200
    assert reset_request.json() == {}
    # Test that JWT is invalidated

def test_request_user_does_not_exist(clear_store, create_user):
    fakeemail = "0" + TEST_USER_EMAIL
    reset_request = requests.post(other.AUTH_PASSWORDRESET_REQUEST_URL, json={"email": fakeemail})
    assert reset_request.status_code == 200
    assert reset_request.json() == {}
