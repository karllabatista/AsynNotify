from fastapi import FastAPI
from starlette import status
from interface.schemas.notification_input import NotificationInput
from interface.schemas.notification_response import NotificationResponse
from interface.schemas.error_response import ErrorResponse
from use_cases.publish_notification import PublishNotificationUseCase
from domain.entities.notification_request import NotificationRequest
from infrastructure.messaging.in_memory_event_bus import InMemoryQueueEventBus
import logging

logging.basicConfig(level=logging.info)
logger = logging.getLogger(__name__)
app = FastAPI()

@app.get("/desempregada")
def hello_world():

    return {"message":"bosta de vida"}

@app.post("/notifications",
          status_code=status.HTTP_200_OK,
          responses={  
            400: {"model": ErrorResponse, "description": "Validation Error"},
            500: {"model": ErrorResponse, "description": "Internal Error"},})
def send_notification(notification_input: NotificationInput):
  
  event_bus = InMemoryQueueEventBus()
  notification_req = NotificationRequest(user_id=notification_input.user_id,
                                    channel=notification_input.channel,
                                    message=notification_input.message)
  
  publish_notification_use_case = PublishNotificationUseCase(event_bus)
  publish_notification_use_case.execute(notification_req)
  return NotificationResponse(message="Notification sent successfully")