import pytest
import requests
import allure
import test_reqres_1_my_token
from datetime import datetime

@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('User Registration Feature')
@allure.suite('User Registration Suite')
@allure.title('Test Registration with Missing Password')
@allure.description('Test the API response when trying to register a user with missing password.')
@allure.severity(allure.severity_level.NORMAL)
def test_register_user_negative():

    url = f'https://reqres.in/api/register/'
    body = {
        'email': 'sydney@fife'
    }

    with allure.step('Send POST request to register user with missing password'):
        response = requests.post(url, json=body)

    with allure.step('Verify the status code is 400'):
        assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}. Response body: {response.text}"

    with allure.step('Verify the error message is "Missing password"'):
        try:
            response_json = response.json()
        except ValueError:
            pytest.fail(f"Response is not in JSON format. Response body: {response.text}")

        assert response_json.get('error') == 'Missing password', f"Expected error message 'Missing password' but got {response_json.get('error')}. Response body: {response.text}"


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('User Authentication Feature')
@allure.suite('Login Suite')
@allure.title('Test Successful Login')
@allure.description('Verify that user can successfully log in with valid credentials.')
@allure.severity(allure.severity_level.NORMAL)
def test_successful_login():

    body = {
        'email': 'eve.holt@reqres.in',
        'password': 'cityslicka'
    }
    headers = {'Content-Type': 'application/json'}

    with allure.step('Send POST request to login endpoint'):
        response = requests.post(
            'https://reqres.in/api/login',
            json=body,
            headers=headers
        )

    with allure.step('Verify response status code is 200'):
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}. Response body: {response.text}"

    with allure.step('Parse the response JSON'):
        try:
            response_json = response.json()
        except ValueError:
            pytest.fail(f"Response is not in JSON format. Response body: {response.text}")

    with allure.step('Check that response JSON contains "token"'):
        assert 'token' in response_json, "Response JSON does not contain 'token'"

    with allure.step('Verify the token matches the expected value'):

        assert response_json['token'] == test_reqres_1_my_token.user_token, f"Expected token '{test_reqres_1_my_token.user_token} but got '{response_json['token']}'"

@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('User Authentication Feature')
@allure.suite('Login Suite')
@allure.title('Test Login with Missing Password')
@allure.description('Verify that login attempt with missing password returns the appropriate error message.')
@allure.severity(allure.severity_level.NORMAL)
def test_login_missing_password():

    url = 'https://reqres.in/api/login'
    body = {
        "email": "peter@klaven"
    }
    headers = {'Content-Type': 'application/json'}

    with allure.step('Send POST request to login endpoint with missing password'):
        response = requests.post(url, json=body, headers=headers)

    with allure.step('Verify response status code is 400'):
        assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}. Response body: {response.text}"

    with allure.step('Parse the response JSON'):
        try:
            response_json = response.json()
        except ValueError:
            pytest.fail(f"Response is not in JSON format. Response body: {response.text}")

    with allure.step('Check that response JSON contains "error"'):
        assert 'error' in response_json, "Response JSON does not contain 'error'"

    with allure.step('Verify the error message'):
        assert response_json['error'] == 'Missing password', f"Expected error 'Missing password' but got {response_json['error']}"


my_id = 0


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('User Creation Feature')
@allure.suite('User Creation Suite')
@allure.title('Test Create User')
@allure.description('Verify that a new user can be created with the correct details and that the response is valid.')
@allure.severity(allure.severity_level.NORMAL)
def test_create_user():

    url = 'https://reqres.in/api/users'
    body = {
        "name": "morpheus",
        "job": "leader"
    }
    headers = {'Content-Type': 'application/json'}

    with allure.step('Send POST request to create user'):
        response = requests.post(url, json=body, headers=headers)

    with allure.step('Verify response status code is 201'):
        assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}. Response body: {response.text}"

    response_json = response.json()

    with allure.step('Verify the name in the response'):
        assert response_json['name'] == body['name'], f"User name does not match. Expected '{body['name']}' but got '{response_json['name']}'"

    with allure.step('Verify the job in the response'):
        assert response_json['job'] == body['job'], f"User job does not match. Expected '{body['job']}' but got '{response_json['job']}'"

    with allure.step('Verify the presence of "id" in the response'):
        assert 'id' in response_json, "Response JSON does not contain 'id'"

    with allure.step('Verify the presence of "createdAt" in the response'):
        assert 'createdAt' in response_json, "Response JSON does not contain 'createdAt'"

    global my_id
    my_id = response_json['id']

    print(f"Created ID: ID={my_id}")

    with allure.step('Verify the format of "createdAt"'):
        created_at = response_json['createdAt']
        try:
            # Convert to ISO 8601 format for validation
            datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except ValueError:
            pytest.fail(f"Invalid datetime format in 'createdAt': {created_at}")

