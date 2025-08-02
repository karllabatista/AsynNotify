from fastapi import FastAPI
from starlette import status
from interface.schemas.notification_input import NotificationInput
from interface.schemas.notification_response import NotificationResponse
from interface.schemas.error_response import ErrorResponse
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
    
  return NotificationResponse(message="Notification sent successfully")