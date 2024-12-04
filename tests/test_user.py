import pytest
from unittest.mock import patch
import requests

# Mock function to replace `requests.get`
def mock_requests_get(url, params):
    # Simulate behavior based on parameters
    if params == {"username": "admin", "password": "admin"}:
        # Unauthorized response
        class MockResponse:
            status_code = 401
            text = ""
        return MockResponse()
    elif params == {"username": "admin", "password": "qwerty"}:
        # Authorized response
        class MockResponse:
            status_code = 200
            text = ""
        return MockResponse()
    else:
        # Default response
        class MockResponse:
            status_code = 404
            text = "Not Found"
        return MockResponse()

# Test function for unauthorized access
@patch('requests.get', side_effect=mock_requests_get)
def test_users_endpoint_unauthorized(mock_get):
    """
    Test the /users endpoint for unauthorized access.
    """
    url = "http://127.0.0.1:8000/users"
    params = {"username": "admin", "password": "admin"}
    
    response = requests.get(url, params=params)
    
    # Assertions
    assert response.status_code == 401, f"Expected status code 401 but got {response.status_code}"
    assert response.text == "", f"Expected an empty response body but got: {response.text}"

# Test function for authorized access
@patch('requests.get', side_effect=mock_requests_get)
def test_users_endpoint_success(mock_get):
    """
    Test the /users endpoint for authorized access.
    """
    url = "http://127.0.0.1:8000/users"
    params = {"username": "admin", "password": "qwerty"}
    
    response = requests.get(url, params=params)
    
    # Assertions
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    assert response.text == "", f"Expected an empty response body but got: {response.text}"

if __name__ == "__main__":
    pytest.main()