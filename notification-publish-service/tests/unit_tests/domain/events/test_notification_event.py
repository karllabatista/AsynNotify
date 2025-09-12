from app.domain.events.notification_event import NotificationEvent
def test_notification_event_create_event_without_request_id():
    
    # ARRANGE + ACT
    event = NotificationEvent(user_id="12345XX",
                              message="Notification sent",
                              channel="sms",
                              destination="testuser@gmail.com")
    event_dict = event.to_dict()

    # ASSERT    
    assert event_dict["event_id"] is not None
    assert event_dict["event_type"] ==  "NotificationCreated"
    assert "timestamp" in event_dict
    assert "payload" in event_dict
    assert event_dict["payload"]["user_id"] == "12345XX"
    assert event_dict["payload"]["message"] == "Notification sent"
    assert event_dict["payload"]["channel"] == "sms"
    assert event_dict["payload"]["destination"] == "testuser@gmail.com"

def test_notification_event_create_event_with_request_id():
    
    # ARRANGE + ACT
    event = NotificationEvent(user_id="12345XX",
                              message="Notification sent",
                              channel="sms",
                              destination="testuser@gmail.com",
                              request_id="3fa85f64-5717-4562-b3fc-2c963f66afa6")
    event_dict = event.to_dict()

    # ASSERT    
    assert event_dict["event_id"] is not None
    assert event_dict["event_type"] ==  "NotificationCreated"
    assert "timestamp" in event_dict
    assert "payload" in event_dict
    assert event_dict["payload"]["user_id"] == "12345XX"
    assert event_dict["payload"]["message"] == "Notification sent"
    assert event_dict["payload"]["channel"] == "sms"
    assert event_dict["payload"]["destination"] == "testuser@gmail.com"
    assert event_dict["request_id"] == "3fa85f64-5717-4562-b3fc-2c963f66afa6"