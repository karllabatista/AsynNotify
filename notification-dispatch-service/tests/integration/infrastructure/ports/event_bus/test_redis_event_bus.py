from src.infrastructure.ports.event_bus.redis_event_bus import RedisEventBus
import redis
import json
def test_redis_event_bus_consumer_event():

    # Arrange

    redis_client =redis.Redis(host="localhost",port=6379,db=0)
    queue = "notification"
    timeout = 10

    # PUBLIC EVENT IN QUEUE

    event = {"type":"test","payload":"ok"}
    redis_client.lpush(queue,json.dumps(event))

    #ACT
    consumer = RedisEventBus(redis_client,queue,timeout)

    result = consumer.consumer_event()


    # ASSERT
    assert isinstance(result,dict)
    assert "type" in result
    assert "payload" in result
    assert result["type"] == "test"
    assert result["payload"] == "ok"


