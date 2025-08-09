from src.infrastructure.ports.event_bus.redis_event_bus import RedisEventBus
import redis
import json
import pytest

@pytest.fixture
def redis_client():

    # Arrange

    client =redis.Redis(host="localhost",port=6379,db=0)
    queue = "notifications_test"

    client.delete(queue) # clear queue before test
    yield client
    client.delete(queue) # clear queue after test


def test_redis_event_bus_consumer_event(redis_client):

    # PUBLIC EVENT IN QUEUE
    timeout = 5
    queue = "notifications_test"

    event = {
    "event_type": "notification_sent",
    "data": {
        "user_id": "123",
        "message": "Hello World",
        "channel": "email",
        "destination": "user@example.com"
    },
    "metadata": {
        "timestamp": "2025-08-09T13:00:00Z",
        "request_id": "012030"
    }
}
    redis_client.lpush(queue,json.dumps(event))

    #ACT
    consumer = RedisEventBus(redis_client,queue,timeout)

    result = consumer.consumer_event()


    # ASSERT
    assert isinstance(result,dict)
    assert "data" in result
    assert "metadata" in result
    assert result["data"]["user_id"] == "123"
    assert result["data"]["message"] == "Hello World"
    assert result["data"]["channel"] == "email"
    assert result["data"]["destination"] ==  "user@example.com"


