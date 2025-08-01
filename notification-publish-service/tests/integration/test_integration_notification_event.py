from domain.entities.notification_request import NotificationRequest
from domain.events.notification_event import NotificationEvent
def test_notifiction_event_integration_with_real_notification_request():
        
        # arranje 
        notification_request = NotificationRequest(
                               user_id="user104@",
                               channel="email",
                               message="sua compra foi finalizada com sucesso"

                                )
        # act
        event = NotificationEvent(notification_request)
        result = event.to_dict()

        # assert

        assert result["event_type"] == "NotificationRequested"
        assert result["data"]["user_id"] == "user104@"
        assert result["data"]["channel"] == "email"
        assert result["data"]["message"] == "sua compra foi finalizada com sucesso"
        assert "request_id" in result["metadata"]
        assert "timestamp" in result["metadata"]

