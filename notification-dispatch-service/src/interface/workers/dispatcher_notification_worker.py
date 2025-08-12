from src.application.use_cases.dispatch_notification import DispatchNotificationUseCase
from src.infrastructure.ports.event_bus.redis_event_bus import RedisEventBus
from src.application.services.notification_factory import NotificationFactory
from src.infrastructure.ports.dispatchers.channel_dispatch_router import ChannelDispatchRouter
from src.infrastructure.ports.dispatchers.email_channel_dispatch import EmailChannelDispatch
from src.infrastructure.ports.services.faker_email_service import FakerEmailService
from src.domain.exceptions.empty_queue_exception import EmptyQueueException
import redis.asyncio as aioredis
import asyncio
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_worker():
    logger.info("Dispatch Notification Worker started. Listening queue...")
    
    QUEUE_NAME = "notifications"
    redis_client = await aioredis.from_url("redis://localhost:6379",db=0,decode_responses=True)
    consumer = RedisEventBus(redis_client,QUEUE_NAME,timeout=5)
    
    # call notification object factory
    notification_factory = NotificationFactory()


    service = FakerEmailService()

    dispatchers = {
        "email":EmailChannelDispatch(service)
        
    }
    channel_dispatch = ChannelDispatchRouter(dispatchers)


    use_case = DispatchNotificationUseCase(consumer,notification_factory,channel_dispatch)
    
    
    logger.info("Dispatch Notification Worker started. Listening queue...")
    while True:
        try:
            # TODO BACKOFF OU LIMIT TRY
                await use_case.execute()
        except EmptyQueueException:
            logger.info("The queue is empty")

        except Exception as e:
            logger.exception(f"Erro no processamento: {e}")
            await asyncio.sleep(1)  
