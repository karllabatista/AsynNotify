from app.domain.events.notification_event import NotificationEvent
from app.infrastructure.messaging.kafka_event_bus import KafkaEventBus,TOPIC
from app.domain.exceptions.event_bus_exceptions import EventBusPermanentError,EventBusTemporaryError,EventBusError
from confluent_kafka.error import ProduceError,KafkaException
from config.env import get_kafka_topic_name
import json
import pytest
from unittest.mock import MagicMock
import json
import logging
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

    producer = MagicMock()
    
    return KafkaEventBus(producer)
    
  
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


def test_delivery_report_success(caplog,event_bus):
    

    # caplog to capture and logging output from a test

    caplog.set_level(logging.INFO)
    msg = MagicMock()
    event_bus._delivery_report(err=None,msg=msg)

    assert "Message produced:" in caplog.text
    assert str(msg) in caplog.text

    
def test_delivery_report_failure(caplog,event_bus):
    

    # caplog to capture and logging output from a test

    caplog.set_level(logging.INFO)
    msg = MagicMock()

    event_bus._delivery_report(err="some-error",msg=msg)

    assert "Failed to deliver message" in caplog.text
    assert str(msg) in caplog.text


def test_publish_event_with_success_delivery_report(event,event_bus,caplog):
    # arrange
    caplog.set_level(logging.INFO)

    def fake_produce(TOPIC,key,value,callback):
        callback(err=None,msg="fake-msg")

    event_bus.producer.produce.side_effect = fake_produce

    
    # act
    event_bus.publish(event)    
    # assert

    assert "Message produced:" in caplog.text
    event_bus.producer.flush.assert_called_once_with(timeout=5)


def test_publish_event_with_failed_delivery_report(event,event_bus,caplog):
    # arrange
    caplog.set_level(logging.ERROR)

    def fake_produce(TOPIC,key,value,callback):
        callback(err="some-error",msg="fake-mg")

    event_bus.producer.produce.side_effect = fake_produce

    
    # act
    event_bus.publish(event)    
    # assert

    assert "Failed to deliver message" in caplog.text
    assert "some-error" in caplog.text
    event_bus.producer.flush.assert_called_once_with(timeout=5)


def test_publish_event_when_buffer_is_full(event,event_bus):
    
    # arrange

    event_bus.producer.produce.side_effect = BufferError("Buffer is full")

    # act + assert
    with pytest.raises(EventBusTemporaryError,match="Kafka buffer full"):
        event_bus.publish(event)


def test_publish_event_when_payload_is_invalid(event,event_bus):
    
    event_bus.producer.produce.side_effect = ValueError ("Payload error")


    with pytest.raises(EventBusPermanentError,match="Invalid payload"):
        event_bus.publish(event)

def test_publish_event_when_producer_error(event,event_bus):
    
    event_bus.producer.produce.side_effect = ProduceError("producer Internal error")


    with pytest.raises(EventBusTemporaryError,match="Kafka internal error"):
        event_bus.publish(event)

def test_publish_event_when_occurs_kafka_exception(event, event_bus):
    event_bus.producer.produce.side_effect = KafkaException("internal kafka error")

    with pytest.raises(EventBusTemporaryError, match="Kafka internal error"):
        event_bus.publish(event)

def test_publish_event_when_occurs_an_internal_error(event, event_bus):
    event_bus.producer.produce.side_effect =Exception("[Kafka Producer] An error occurred when trying publish event")

    with pytest.raises(EventBusError, match="Unexpected error in KafkaEventBus"):
        event_bus.publish(event)

