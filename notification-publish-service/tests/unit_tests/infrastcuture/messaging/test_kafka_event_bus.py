from app.domain.events.notification_event import NotificationEvent
from app.infrastructure.messaging.kafka_event_bus import KafkaEventBus,TOPIC
import pytest
from unittest.mock import MagicMock
import json

@pytest.fixture
def event():
    return NotificationEvent(
        user_id="test-user",
        message="welcome, user!",
        channel="email",
        destination="testuser@gmail.com"
    )

@pytest.fixture
def event_bus():
    conf = {"bootstrap.servers": "fake"}
    producer = MagicMock()
    
    return KafkaEventBus(conf, producer)
    
  
def test_publish_notification_in_broker_kafka_success(event,event_bus):
    
    # act 
  
    event_bus.publish(event)


    # assert
    key = event.user_id
    payload = json.dumps(event.to_dict())

    event_bus.producer.produce.assert_called_once_with(
        TOPIC,     
        key = key,
        value = payload,
        callback = event_bus._delivery_report
    )

    event_bus.producer.flush.assert_called_once_with(timeout=5)