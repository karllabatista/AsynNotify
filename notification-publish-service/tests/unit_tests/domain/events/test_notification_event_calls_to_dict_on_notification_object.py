from domain.events.notification_event import NotificationEvent
from unittest.mock import Mock
def test_notification_event_to_dict_with_request_id():
    
    request_id_mock = "request-123455"
    notification_request_mock = Mock()
    notification_request_mock.to_dict.return_value ={
        "user_id" :"karlla12345",
        "message": "recebemos seu pedido",
        "channel":"email"
    }


    notification_event = NotificationEvent(notification_request_mock,request_id_mock)
    notification_event.to_dict()

    notification_request_mock.to_dict.assert_called_once_with()
    