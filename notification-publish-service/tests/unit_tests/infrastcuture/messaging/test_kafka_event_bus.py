from app.domain.events.notification_event import NotificationEvent
from app.infrastructure.messaging.kafka_event_bus import KafkaEventBus,TOPIC
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
