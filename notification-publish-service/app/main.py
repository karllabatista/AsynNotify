from fastapi import FastAPI, HTTPException,Depends
from fastapi.responses import JSONResponse
from starlette import status
from interface.schemas.notification_input import NotificationInput
from interface.schemas.notification_response import NotificationResponse
from interface.schemas.error_response import ErrorResponse
from use_cases.publish_notification import PublishNotificationUseCase
from domain.entities.notification_request import NotificationRequest
from infrastructure.messaging.in_memory_event_bus import InMemoryQueueEventBus
from domain.exceptions.notification_publish_error import NotificationPublishError
import logging

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)
app = FastAPI()

event_bus = InMemoryQueueEventBus() # shared queue

@app.get("/healthy")
def hello_world():

    return {"message":"server is working .."}
def get_publish_notification_use_case() -> PublishNotificationUseCase:
   
    return PublishNotificationUseCase(event_bus)

@app.post("/notifications",
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
    except NotificationPublishError as notification_error:
        logger.exception(f"Failed to publish notification:{notification_error}")
        return JSONResponse(status_code=500,content=ErrorResponse(detail=notification_error.message).model_dump())
    except Exception as error:
        logger.exception(f"Failed to publish notification:{error}")
        raise HTTPException(status_code=500,detail="Internal error: Failed to publish notification")