from pydantic import BaseModel,Field
from enum import Enum

class ChannelEnum(str,Enum):
    email = "email"
    sms = "sms"
    push = "push"

class NotificationInput(BaseModel):
    
    user_id:str = Field(...,min_length=1,max_length=20,example="user1234")
    channel:ChannelEnum= Field(...,example="email")
    message: str =Field(...,min_length=1,max_length=200,example ="Sua fatura está disponível.")

    class config:
        schema_extra ={
            "example":{
                "user_id": "abc-123",
                "channel": "email",
                "message": "Você tem uma nova mensagem."
            }
        }