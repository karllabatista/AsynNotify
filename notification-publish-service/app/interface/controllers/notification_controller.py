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
from app.infrastructure.repositories.user_service_contact_info_repository import UserServiceContactInfoRepository
from app.domain.exceptions.user_not_found_exception import UserNotFound
from app.domain.exceptions.external_server_exception import ExternalServiceException
import logging
from config.env import get_base_url_user_service

BASE_URL = get_base_url_user_service()

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/healthy")
def hello_world():

    return {"message":"server is working .."}

def get_publish_notification_use_case() -> PublishNotificationUseCase:
    redis_client = get_redis_connection()
    event_bus = RedisEventBus(redis_client)

    user_contact_info_repository = UserServiceContactInfoRepository(BASE_URL)
    return PublishNotificationUseCase(event_bus,user_contact_info_repository)

@router.post("/notifications",
          status_code=status.HTTP_200_OK,
          responses={  
                400: {"model": ErrorResponse, "description": "Validation Error"},
                404: {"model": ErrorResponse, "description": "User not found"},
                500: {"model": ErrorResponse, "description": "Internal Server Error"},
                503: {"model": ErrorResponse, "description": "External Service Unavailable"},})
def publish_notification(notification_input: NotificationInput,
                      notification_use_case:PublishNotificationUseCase = Depends(get_publish_notification_use_case)):
    try:
        logger.info(f"Received notification request:user_id={notification_input.user_id},channel={notification_input.channel}")
        
        notification_req = NotificationRequest(user_id=notification_input.user_id,
                                          channel=notification_input.channel.value,
                                          message=notification_input.message)
        
        notification_use_case.execute(notification_req)

        return NotificationResponse(message="Notification sent successfully")
    except UserNotFound:
        logger.warning(f"[INTERFACE] User not found: {notification_input.user_id}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=ErrorResponse(detail="User not found").model_dump())
    except ExternalServiceException as external_error:
        logger.error(f"[INTERFACE]  User Service is unavailable:{external_error}")
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content=ErrorResponse(detail="User Service is is temporaril unavailable").model_dump())

    
    except ServerUnavailable as server_error:
         logger.error(f"[INTERFACE]  Failed to publish notification:{server_error}")
         return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content=ErrorResponse(detail="Service temporarily unavailable: Redis connection error").model_dump())
    
    except NotificationPublishError as notification_error:
        logger.error(f"[INTERFACE] Failed to publish notification to queue:{ notification_error}")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(detail="Failed to publish notification").model_dump())
    
    except Exception as error:
        logger.exception(f"Failed to publish notification:{error}")
        raise HTTPException(status_code=500,detail="Internal error: Failed to publish notification")