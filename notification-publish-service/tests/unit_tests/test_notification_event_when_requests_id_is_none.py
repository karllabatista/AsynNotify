from unittest.mock import Mock
from domain.events.notification_event import NotificationEvent
def test_notification_event_when_requests_id_is_none():

    notification_request_mock = Mock()
    notification_request_mock.to_dict.return_value ={
        "user_id" :"karlla12345",
        "message": "recebemos seu pedido",
        "channel":"email"
    }


    notification_event = NotificationEvent(notification_request_mock)
    result_data = notification_event.to_dict()

    result_id = result_data["metadata"]["request_id"]

    assert isinstance(result_id,str)
    assert len(result_id) > 0