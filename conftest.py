import pytest
import requests
import allure


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('User Registration Feature')
@allure.suite('User Registration Suite')
@allure.title('Register User and Retrieve Token')
@allure.description('Test to register a user and retrieve an authentication token.')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.fixture()
def registered_user():
    """
    Fixture to register a user and return their ID and token.
    """
    url = 'https://reqres.in/api/register'
    body = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    headers = {'Content-Type': 'application/json'}

    with allure.step('Send POST request to register user'):
        response = requests.post(url, headers=headers, json=body)

    with allure.step('Verify the response status code is 200'):
        assert response.status_code == 200, f'Expected status code 200 but got {response.status_code}. Response body: {response.text}'

    response_json = response.json()

    with allure.step('Check that response contains "id"'):
        assert "id" in response_json, f"Response does not contain 'id': {response_json}"

    with allure.step('Check that response contains "token"'):
        assert "token" in response_json, f"Response does not contain 'token': {response_json}"

    return {
        "id": response_json["id"],
        "token": response_json["token"]
    }
