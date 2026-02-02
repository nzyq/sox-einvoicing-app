import pytest
import requests
from src.config import url
import src.other as other

@pytest.fixture
def clear_store():
    requests.delete(other.CLEAR_URL, json={})


def test_single_logout_success(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    logout_request = requests.post(other.LOGOUT_URL, json={"token": response.json()['token']})
    assert logout_request.status_code == 200
    assert logout_request.json() == {}


def test_logout_invalid_token(clear_store):
    response = requests.post(other.REGISTER_URL, json={"email":"z55555@unsw.edu.au", "password":"passwordlong", "name_first":"Jake", "name_last":"Renzella"})
    requests.post(other.LOGOUT_URL, json={"token": response.json()['token']})
    logout_request_1 = requests.post(other.LOGOUT_URL, json={"token": response.json()['token']})
    assert logout_request_1.status_code == 403
