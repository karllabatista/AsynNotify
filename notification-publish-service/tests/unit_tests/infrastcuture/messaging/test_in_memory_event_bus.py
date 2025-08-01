from unittest.mock import Mock
from app.infrastructure.messaging.in_memory_event_bus import InMemoryQueueEventBus
from app.domain.entities.notification_request import NotificationRequest
def test_publish_event():
    ## arrange
    
    request_id_mock = "abc1234-00"
    notification_request= NotificationRequest(user_id="karlla.batista",
                                              message="pagamento confirmado",
                                              channel="email")

    ## act
    immemory = InMemoryQueueEventBus()
    result = immemory.publish(notification_request,request_id_mock)


    # assert 
    
    assert result is True
    assert not immemory.queue.empty()
    event_in_queue = immemory.queue.get_nowait()
    assert event_in_queue["event_type"] == "NotificationRequested"
    assert event_in_queue["data"]["user_id"] == "karlla.batista"
    assert event_in_queue["data"]["message"] == "pagamento confirmado"
    assert event_in_queue["data"]["channel"] == "email"
    assert event_in_queue["metadata"]["request_id"] == request_id_mock
    assert "timestamp" in event_in_queue["metadata"]