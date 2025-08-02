from pydantic import BaseModel,Field
class NotificationResponse(BaseModel):
    
    message:str = Field(...,examples="Notification sent successfully")