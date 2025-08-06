from unittest.mock import patch
from app.infrastructure.in_memory_repository import InMemoryRepository
from app.domain.entities.contact_info import ContactInfo
def test_get_user_by_id():

    mock_user_db = {
      
        "mockeruser":{ 
                "contact_info":
                {
                    "email":"mockeruser@gmail.com",
                    "sms":"+55000000000",
                    "preferred_channel":"email"
                }
        
        }

    }
    with patch.object(InMemoryRepository,"USER_DB",mock_user_db):
        inmemory = InMemoryRepository()
        contact = inmemory.get_user_by_id("mockeruser")

        assert isinstance(contact,ContactInfo)
        assert contact.email == "mockeruser@gmail.com"
        assert contact.sms == "+55000000000"
        assert contact.preferred_channel == "email"
    

