from src.application.use_cases.dispatch_notification import DispatchNotificationUseCase
from src.infrastructure.ports.event_bus.redis_event_bus import RedisEventBus
from src.application.services.notification_factory import NotificationFactory
from src.infrastructure.ports.dispatchers.channel_dispatch_router import ChannelDispatchRouter
from src.infrastructure.ports.dispatchers.email_channel_dispatch import EmailChannelDispatch
from src.infrastructure.ports.services.faker_email_service import FakerEmailService
from src.domain.exceptions.empty_queue_exception import EmptyQueueException
from src.infrastructure.ports.redis_client import get_redis_connection
from config.env import get_queue
import asyncio
import logging
import signal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_worker():
    """
    Executes a worker that consumes events from a queue, processes them into notifications,
    and dispatches via specific channels (email, sms, etc).

    raises
             
        Handling forced worker termination.

        This block captures two distinct interruption scenarios:

        1. asyncio.CancelledError:
        - Occurs when an asynchronous task is explicitly canceled
        via `task.cancel()` or when the event loop is being
        finalized.
        - Catching this exception ensures that the worker can terminate
        in a controlled manner, executing cleanup routines before exiting.

        2. KeyboardInterrupt:
        - Raised when the user presses Ctrl+C in the terminal,
        sending an interrupt signal (SIGINT) to the process.
        - Handling this case prevents abrupt termination,
        allowing resources (such as Redis connections) to be released and
        logging termination.

        Both handlers aim to enable a graceful and predictable worker shutdown, even under cancellation
        or manual interruption conditions.
      
    """
    logger.info("Dispatch Notification Worker started. Listening queue...")
    
    QUEUE_NAME = get_queue()
    redis_client = await get_redis_connection()
    consumer = RedisEventBus(redis_client,QUEUE_NAME,timeout=5)
    # call notification object factory
    notification_factory = NotificationFactory()


    service = FakerEmailService()

    dispatchers = {
        "email":EmailChannelDispatch(service)
        
    }
    channel_dispatch = ChannelDispatchRouter(dispatchers)


    use_case = DispatchNotificationUseCase(consumer,notification_factory,channel_dispatch)
    

    # It allows you to make an asynchronous loop run until a “signal” is given.
    # This “signal” is stop_event.set(), which you trigger when you want to stop the worker. 
    stop_event = asyncio.Event()
    def shutdown():
        logger.info("Shutdown signal received. Stopping worker...")
        stop_event.set()

    # Registers a handler for the SIGINT signal (usually sent when pressing Ctrl+C),
    # so that when this signal is received, the `shutdown` function is executed,
    # allowing a controlled and graceful termination of the program.
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown) # ctrc+c
    loop.add_signal_handler(signal.SIGTERM, shutdown) # kill
    
    while not stop_event.is_set():
        try:
            # TODO BACKOFF OU LIMIT TRY
            await use_case.execute()
        except EmptyQueueException:
            logger.info("The queue is empty")
            await asyncio.sleep(1)

        except Exception as e:
            logger.exception(f"Error to process: {e}")
            await asyncio.sleep(1)  
        except (asyncio.CancelledError, KeyboardInterrupt):
            logger.info("Shutdown requested. Cleaning up...")
            break
    
    logger.info("Close connection with Redis...")
    await redis_client.close()
    logger.info("Worker close successfully.")
