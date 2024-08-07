import requests
import pytest
import allure
import test_reqres_2_post

@pytest.mark.smoke
@pytest.mark.regression
@allure.feature('User Management')
@allure.suite('User API Tests')
@allure.title('Delete User by ID')
@allure.description('This test verifies that deleting a user by ID returns a 204 No Content response and confirms that the user is deleted.')
@allure.severity(allure.severity_level.CRITICAL)
def test_delete_user_by_id():
    # Use the ID from test_reqres_2_post or adjust as needed
    user_id = test_reqres_2_post.my_id
    url = f'https://reqres.in/api/users/{user_id}'
    headers = {'Content-Type': 'application/json'}

    with allure.step(f'Send DELETE request to delete user with ID {user_id}'):
        response = requests.delete(url, headers=headers)

    with allure.step('Verify the status code of the response'):
        assert response.status_code == 204, f"Expected status code 204 but got {response.status_code}"

    with allure.step('Verify that no content is returned'):
        assert response.text == '', "Response body is not empty; expected no content."
