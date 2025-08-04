from fastapi import APIRouter, HTTPException,Depends
from fastapi.responses import JSONResponse
from starlette import status
from app.interface.schemas.notification_input import NotificationInput
from app.interface.schemas.notification_response import NotificationResponse
from app.interface.schemas.error_response import ErrorResponse
from app.use_cases.publish_notification import PublishNotificationUseCase
from app.domain.entities.notification_request import NotificationRequest
from app.infrastructure.messaging.redis_event_bus import RedisEventBus
from app.domain.exceptions.notification_publish_error import NotificationPublishError
from app.domain.exceptions.server_unavailable_error import ServerUnavailable
from app.infrastructure.redis_client import get_redis_connection
import logging


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/healthy")
def hello_world():

    return {"message":"server is working .."}

def get_publish_notification_use_case() -> PublishNotificationUseCase:
    redis_client = get_redis_connection()
    event_bus = RedisEventBus(redis_client)
    return PublishNotificationUseCase(event_bus)

@router.post("/notifications",
          status_code=status.HTTP_200_OK,
          responses={  
            400: {"model": ErrorResponse, "description": "Validation Error"},
            500: {"model": ErrorResponse, "description": "Internal Error"},})
def publish_notification(notification_input: NotificationInput,
                      notification_use_case:PublishNotificationUseCase = Depends(get_publish_notification_use_case)):
    try:
        logger.info(f"Received notification request:user_id={notification_input.user_id},channel={notification_input.channel}")
        
        notification_req = NotificationRequest(user_id=notification_input.user_id,
                                          channel=notification_input.channel,
                                          message=notification_input.message)
        
        notification_use_case.execute(notification_req)
        return NotificationResponse(message="Notification sent successfully")
    except ServerUnavailable as server_error:
         logger.error(f"Failed to publish notification:{server_error}")
         return JSONResponse(
            status_code=503,
            content=ErrorResponse(detail="Service temporarily unavailable: Redis connection error").model_dump()
        )
    except NotificationPublishError as notification_error:
        logger.error(f"Failed to publish notification:{notification_error}")
        return JSONResponse(status_code=500,content="Failed to publish notification")
    
    except Exception as error:
        logger.exception(f"Failed to publish notification:{error}")
        raise HTTPException(status_code=500,detail="Internal error: Failed to publish notification")