import requests
import pytest
import allure
import test_reqres_1_my_token

@pytest.mark.regression
@allure.feature('User Management')
@allure.suite('User API Tests')
@allure.title('Get Single User by ID')
@allure.description('This test verifies that a single user can be fetched by their ID from the ReqRes API and checks that the user details are correct.')
@allure.severity(allure.severity_level.CRITICAL)
def test_get_single_user_by_id():
    headers = {'Content-Type': 'application/json'}
    single_user_id = test_reqres_1_my_token.user_id

    with allure.step(f'Send GET request to fetch user by ID {single_user_id}'):
        response = requests.get(f'https://reqres.in/api/users/{single_user_id}', headers=headers)

    with allure.step('Verify the status code of the response'):
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    response_json = response.json()

    with allure.step('Verify the presence of "data" in response JSON'):
        assert 'data' in response_json, "Response JSON does not contain 'data'"

    with allure.step('Verify the user ID in the response data'):
        assert response_json['data']['id'] == single_user_id, "User ID does not match"


@pytest.mark.regression
@allure.feature('User Management')
@allure.suite('User API Tests')
@allure.title('Get Non-Existent User by ID')
@allure.description('This test verifies that attempting to fetch a user with a non-existent ID returns a 404 status code.')
@allure.severity(allure.severity_level.CRITICAL)
def test_get_user_by_id_not_found():
    headers = {'Content-Type': 'application/json'}
    non_existent_user_id = 23

    with allure.step(f'Send GET request to fetch non-existent user with ID {non_existent_user_id}'):
        response = requests.get(f'https://reqres.in/api/users/{non_existent_user_id}', headers=headers)

    with allure.step('Verify the status code of the response'):
        assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"


@pytest.mark.regression
@allure.feature('User API')
@allure.story('Get Users - Page 2')
@allure.title('Get Users on Page 2')
@allure.description('This test verifies that the users on page 2 are returned correctly from the ReqRes API.')
def test_get_users_page_2():
    url = 'https://reqres.in/api/users'
    params = {'page': 2}

    with allure.step('Send GET request to fetch users on page 2'):
        response = requests.get(url, params=params)

    with allure.step('Verify the status code of the response'):
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

    data = response.json()

    with allure.step('Validate the JSON structure'):
        assert data['page'] == 2, f"Expected page 2 but got {data['page']}"
        assert data['per_page'] == 6, f"Expected per_page 6 but got {data['per_page']}"
        assert data['total'] == 12, f"Expected total 12 but got {data['total']}"
        assert data['total_pages'] == 2, f"Expected total_pages 2 but got {data['total_pages']}"

    with allure.step('Validate the user data'):
        assert len(data['data']) == 6, f"Expected 6 users but got {len(data['data'])}"

        user = data['data'][0]
        assert user['email'] == "michael.lawson@reqres.in", f"Expected email michael.lawson@reqres.in but got {user['email']}"
        assert user['first_name'] == "Michael", f"Expected first_name Michael but got {user['first_name']}"
        assert user['last_name'] == "Lawson", f"Expected last_name Lawson but got {user['last_name']}"
        assert user['avatar'] == "https://reqres.in/img/faces/7-image.jpg", f"Expected avatar URL https://reqres.in/img/faces/7-image.jpg but got {user['avatar']}"
