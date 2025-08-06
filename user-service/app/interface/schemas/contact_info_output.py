from pydantic import BaseModel
from app.domain.entities.contact_info import ContactInfo
class ContactInfoOutput(BaseModel):

    email: str
    sms: str
    preferred_channel:str
    
    @classmethod
    def from_entity(cls,contact:ContactInfo)-> "ContactInfoOutput":
        return cls(email=contact.email, sms=contact.sms,preferred_channel=contact.preferred_channel)
