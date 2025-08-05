from unittest.mock import patch,MagicMock
from app.infrastructure.repositories.user_service_contact_info_repository import UserServiceContactIndoRepository
@patch("app.infrastructure.repositories.user_service_contact_info_repository.requests.get")
def test_user_service_contact_info_repository(mock_get):
    # Arrange
    mock_response_data = {
        "email": "karlla@example.com",
        "sms": "+559299999999",
        "preferred_channel": "email"
    }

    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    mock_get.return_value = mock_response

    user_service = UserServiceContactIndoRepository(base_url="http://fake-url")
    result= user_service.get_contact_info_by_user_id("123")

    # Assert
    mock_get.assert_called_once_with("http://fake-url/users/123/contact-info")
    assert isinstance(result,dict)
    assert result["email"] == "karlla@example.com"
    assert result["sms"] == "+559299999999"
    assert result["preferred_channel"] == "email"