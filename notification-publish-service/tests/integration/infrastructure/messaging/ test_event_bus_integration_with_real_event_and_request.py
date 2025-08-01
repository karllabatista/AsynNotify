from app.infrastructure.messaging.in_memory_event_bus import InMemoryQueueEventBus
from app.domain.entities.notification_request import NotificationRequest
from app.domain.events.notification_event import NotificationEvent
from app.domain.exceptions.notification_publish_error import NotificationPublishError

def test_event_bus_integration_with_real_event_and_request():
    # Arrange: criar os objetos reais
    request_id = "req-001"
    notification = NotificationRequest(
        user_id="karlla.batista",
        message="Pagamento confirmado",
        channel="email"
    )
    event_bus = InMemoryQueueEventBus()

    # Act: publicar o evento
    result = event_bus.publish(notification, request_id)

    # Assert
    assert result is True
    assert not event_bus.queue.empty()

    event_dict = event_bus.queue.get_nowait()

    # Checa se os campos essenciais foram propagados
    assert event_dict["user_id"] == "karlla.batista"
    assert event_dict["message"] == "Pagamento confirmado"
    assert event_dict["channel"] == "email"
    assert event_dict["request_id"] == request_id
    assert "timestamp" in event_dict
