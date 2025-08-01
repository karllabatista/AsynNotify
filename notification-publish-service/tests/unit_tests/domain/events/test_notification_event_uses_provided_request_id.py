from unittest.mock import Mock
from domain.events.notification_event import NotificationEvent
def test_notification_event_uses_provided_request_id():

    request_id_mock = "request-123455"
    notification_request_mock = Mock()
    notification_request_mock.to_dict.return_value ={
        "user_id" :"karlla12345",
        "message": "recebemos seu pedido",
        "channel":"email"
    }


    notification_event = NotificationEvent(notification_request_mock,request_id_mock)
    result_data = notification_event.to_dict()

    assert result_data["metadata"]["request_id"] == request_id_mock