from src.application.use_cases.dispatch_notification import DispatchNotificationUseCase
from src.infrastructure.ports.event_bus.redis_event_bus import RedisEventBus
import redis.asyncio as aioredis
import pytest
import pytest_asyncio
import json
from src.application.services.notification_factory import NotificationFactory
from src.infrastructure.ports.dispatchers.channel_dispatch_router import ChannelDispatchRouter
from src.infrastructure.ports.dispatchers.email_channel_dispatch import EmailChannelDispatch
from src.infrastructure.ports.services.faker_email_service import FakerEmailService
from src.domain.exceptions.invalid_notification_event import InvalidNotificationEvent


QUEUE_NAME = "notificationd-test"

@pytest_asyncio.fixture
async def redis_client():
    client = await aioredis.from_url("redis://localhost:6379",db=0,decode_responses=True)

    await client.delete(QUEUE_NAME) # clear queue before test
    yield client
    await client.delete(QUEUE_NAME) # clear queue after test
@pytest.mark.asyncio  
async def test_dispatch_notification_success(redis_client):
    
    # ARRANJE


    # insert a new event in the queue
    
    event ={
            "event_type": "NotificationRequested",
            "data":{
                "user_id":"user.test",
                "message":" this a test messafe",
                "channel" :"email",
                "destination":"test@test.com"                 
            },
            "metadata":{
                "timestamp":"",
                "request_id": "ABCB-request"
            }
    }
    await redis_client.lpush(QUEUE_NAME,json.dumps(event))

    consumer = RedisEventBus(redis_client,QUEUE_NAME,timeout=5)
  
    # call notification object factory
    notification_factory = NotificationFactory()

    service = FakerEmailService()

    dispatchers = {
        "email":EmailChannelDispatch(service)
        
    }
    channel_dispatch = ChannelDispatchRouter(dispatchers)

    # ACT
    dispatch_use_case = DispatchNotificationUseCase(consumer,
                                                    notification_factory,
                                                    channel_dispatch)
    
    # just checks if it doesn't throw an exception  
    await dispatch_use_case.execute()

    # ASSERT - garante que o envio foi chamado uma vez
    assert service.last_email["destination"] == "test@test.com"

@pytest.mark.asyncio

async def test_dispatch_notification_raises_data_key_missing(redis_client):
    # ARRANJE
    # insert a new event in the queue
    
    event ={
            "event_type": "NotificationRequested",
            "metadata":{
                "timestamp":"",
                "request_id": "ABCB-request"
            }
    }
    await redis_client.lpush(QUEUE_NAME,json.dumps(event))

    consumer = RedisEventBus(redis_client,QUEUE_NAME,timeout=5)
  
    # call notification object factory
    notification_factory = NotificationFactory()

    service = FakerEmailService()

    dispatchers = {
        "email":EmailChannelDispatch(service)
        
    }
    channel_dispatch = ChannelDispatchRouter(dispatchers)

    # ACT + ASSERT

    with pytest.raises(InvalidNotificationEvent) as  excinfo:
        dispatch_use_case = DispatchNotificationUseCase(consumer,
                                                    notification_factory,
                                                    channel_dispatch)
        # just checks if it doesn't throw an exception  
        await dispatch_use_case.execute()

    assert "Missing data key in event" in str(excinfo.value)    