from datetime import datetime,timezone
from uuid import uuid4
class NotificationEvent:
    
    def __init__(self,
                 user_id:str,
                 message:str,
                 channel:str,
                 destination:str,
                 request_id:str = None):
        
        self.event_id = str(uuid4())
        self.event_type = "NotificationCreated"
        self.timestamp = datetime.now(timezone.utc).isoformat() + "Z"
        self.user_id= user_id
        self.message = message
        self.channel= channel
        self.destination = destination    
        self.request_id= request_id or str(uuid4())

    def to_dict(self):
        return{
              "event_id" : self.event_id,
              "event_type": self.event_type,
              "timestamp":self.timestamp,
              "payload":{
                    "user_id":self.user_id,
                    "message":self.message,
                    "channel" :self.channel,
                    "destination":self.destination                  
              },
              "request_id":self.request_id
                   
              }
      