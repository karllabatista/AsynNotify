from src.application.services.notification_factory import NotificationFactory
from src.domain.entitites.notification import Notification
from src.domain.exceptions.invalid_notification_event import InvalidNotificationEvent
import pytest
def test_notification_factory_create_object():

    ## ARRANGE
    event = {
        "event_type": "notification_sent",
        "data": {
            "user_id": "123",
            "message": "Hello World",
            "channel": "email",
            "destination": "user@example.com"
        },
        "metadata": {
            "timestamp": "2025-08-09T13:00:00Z",
            "request_id": "012030"
        }
    }

    # ACT
    notification = NotificationFactory()
    result=notification.create_from_event(event)


    # ASSERT
    assert isinstance(result,Notification)

def test_notification_factory_raise_missing_data_key():
    ## ARRANGE
    event = {
        "event_type": "notification_sent",
        "metadata": {
            "timestamp": "2025-08-09T13:00:00Z",
            "request_id": "012030"
        }
            
    }
    # ACT+ASSERT
    with pytest.raises(InvalidNotificationEvent) as e:
        notification = NotificationFactory()
        notification.create_from_event(event)
    
    assert "Missing data key in event" in str(e.value)

