import requests
import pytest
import allure
from datetime import datetime
import test_reqres_2_post


@pytest.mark.regression
@allure.feature('User Management')
@allure.suite('User API Tests')
@allure.title('Update User Details')
@allure.description('This test verifies that updating user details correctly reflects the changes and includes an updated timestamp.')
@allure.severity(allure.severity_level.CRITICAL)
def test_update_user():
    url = f'https://reqres.in/api/users/{test_reqres_2_post.my_id}'
    body = {
        "name": "morpheus",
        "job": "zion resident"
    }
    headers = {'Content-Type': 'application/json'}

    with allure.step('Send PUT request to update user details'):
        response = requests.put(url, json=body, headers=headers)

    with allure.step('Verify the status code of the response'):
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    with allure.step('Verify the response body contains the updated details'):
        response_json = response.json()
        assert response_json['name'] == body['name'], "User name does not match"
        assert response_json['job'] == body['job'], "User job does not match"

    with allure.step('Verify the response body contains "updatedAt" timestamp'):
        assert 'updatedAt' in response_json, "Response JSON does not contain 'updatedAt'"

        updated_at = response_json['updatedAt']
        try:
            datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        except ValueError:
            pytest.fail(f"Invalid datetime format in 'updatedAt': {updated_at}")

