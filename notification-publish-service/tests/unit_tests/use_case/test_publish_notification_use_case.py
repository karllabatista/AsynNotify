from app.use_cases.publish_notification import PublishNotificationUseCase
from app.domain.entities.contact_info import ContactInfo
from unittest.mock import Mock
from app.domain.exceptions.notification_publish_error import NotificationPublishError
from app.domain.exceptions.user_not_found_exception import UserNotFound
import pytest

def test_execute_when_publish_succeeds_logs_success():
    
    # arrange

    #create fake contact
    fake_contact_info = ContactInfo(
       
        email="test@example.com",
        sms="+5511999999999",
        preferred_channel ="email"
    )

    user_repository_mock = Mock()
    user_repository_mock.get_contact_info_by_user_id.return_value=fake_contact_info
    
    event_bus_mock = Mock()
    event_bus_mock.publish.return_value = True

    notification_dict = {
        "user_id" :"test123",
        "message": " hello test",
        "channel":"sms"
    }

    # act
    publish_notications_uc =  PublishNotificationUseCase(event_bus_mock,user_repository_mock)
    publish_notications_uc.execute(notification_dict)
    
    # assert
    
    event_bus_mock.publish.assert_called_once()


def test_execute_when_publish_returns_false_raises_notification_publish_error():

    
    # arrange

    #create fake contact
    fake_contact_info = ContactInfo(
       
        email="test@example.com",
        sms="+5511999999999",
        preferred_channel ="email"
    )

    user_repository_mock = Mock()
    user_repository_mock.get_contact_info_by_user_id.return_value=fake_contact_info
    
    event_bus_mock = Mock()
    event_bus_mock.publish.return_value = False

    notification_dict = {
        "user_id" :"test123",
        "message": " hello test",
        "channel":"sms"
    }

    
 
    #act
    with pytest.raises(NotificationPublishError) as error_info:
        publish_notications_uc =  PublishNotificationUseCase(event_bus_mock,user_repository_mock)
        publish_notications_uc.execute(notification_dict)
    
    # assert
    assert str(error_info.value) == "Failed to publish event"

def test_execute_when_publish_raises_exception_raises_notification_publish_error():
    # arrange

    #create fake contact
    fake_contact_info = ContactInfo(
       
        email="test@example.com",
        sms="+5511999999999",
        preferred_channel ="email"
    )

    user_repository_mock = Mock()
    user_repository_mock.get_contact_info_by_user_id.return_value=fake_contact_info
    
    event_bus_mock = Mock()
    event_bus_mock.publish.side_effect = Exception()

    notification_dict = {
        "user_id" :"test123",
        "message": " hello test",
        "channel":"sms"
    }

    publish_notications_uc =  PublishNotificationUseCase(event_bus_mock,user_repository_mock)

    with pytest.raises(Exception) as exc_info:
       publish_notications_uc.execute(notification_dict)

    assert "Failed to publish event" in str(exc_info.value)

def test_execute_when_user_is_not_found_raise_user_not_found_exception():
    # arrange

    #create fake contact
    fake_contact_info = ContactInfo(
       
        email="test@example.com",
        sms="+5511999999999",
        preferred_channel ="email"
    )

    user_repository_mock = Mock()
    user_repository_mock.get_contact_info_by_user_id.return_value={}
    event_bus_mock = Mock()


    notification_dict = {
        "user_id" :"test123",
        "message": " hello test",
        "channel":"sms"
    }

    # act+assert
    publish_notications_uc =  PublishNotificationUseCase(event_bus_mock,user_repository_mock)
    
    with pytest.raises(UserNotFound) as exec_info:
        publish_notications_uc.execute(notification_dict)
    
    assert "[PUBLISH SERVICE] User not found" in str(exec_info.value)
