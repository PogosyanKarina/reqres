import requests
import pytest
import allure

user_id = None
user_token = None
user_email = None

@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('User Registration Feature')
@allure.suite('User Registration Suite')
@allure.title('Test Registration with Valid Credentials')
@allure.description('Test the API response when trying to register a user with valid credentials.')
@allure.severity(allure.severity_level.NORMAL)
def test_reqres_create_token():
    global user_id, user_token, user_email
    body = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    headers = {'Content-Type': 'application/json'}

    with allure.step('Send POST request to register endpoint'):
        response = requests.post(
            'https://reqres.in/api/register',
            headers=headers,
            json=body
        )

    with allure.step('Verify response status code is 200'):
        assert response.status_code == 200, f'Expected status code 200 but got {response.status_code}. Response body: {response.text}'

    with allure.step('Parse the response JSON'):
        try:
            response_json = response.json()
        except ValueError:
            pytest.fail(f"Response is not in JSON format. Response body: {response.text}")

    with allure.step('Check that response JSON contains "id"'):
        assert "id" in response_json, f"Response does not contain 'id': {response_json}"

    with allure.step('Check that response JSON contains "token"'):
        assert "token" in response_json, f"Response does not contain 'token': {response_json}"

    user_id = response_json["id"]
    user_token = response_json["token"]
    user_email = body['email']

    print(f"Registration details: ID={user_id}, Token={user_token}, Email={user_email}")


