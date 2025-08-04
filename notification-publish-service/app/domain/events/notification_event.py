from datetime import datetime,timezone
from uuid import uuid4
from app.domain.entities.notification_request import NotificationRequest
class NotificationEvent:
    
    def __init__(self,notification:NotificationRequest,request_id:str=None):
        self.notification = notification.to_dict()
        self.event_type = "NotificationRequested"
        self.request_id= request_id or str(uuid4())
        self.metadata = {
                        "timestamp":datetime.now(timezone.utc).isoformat() + "Z",
                        "request_id":self.request_id
                      }

    def to_dict(self):
        return{
              "event_type": self.event_type,
              "data":self.notification,
              "metadata":self.metadata
                   
              }
      