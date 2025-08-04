from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.contact_info import ContactInfo 
class InMemoryRepository(UserRepository):
    # Indexed by user_id
    USER_DB = {
            
                "karlla":{ 
                    
                    "contact_info":{
                        "email":"karllabatista19@gmail.com",
                        "sms":"+5592991353213",
                        "prefered_channel":"email"
                    }
                },
                "caiocrux":{
                  
                    "contact_info":{
                        "email":"caio.crux@gmail.com",
                        "sms":"+559292846992",
                        "prefered_channel":"sms"
                    }  
                }
            
        }
       
    
    def get_user_by_id(self,user_id:str)-> ContactInfo:
        
        user_contacto_info = InMemoryRepository.USER_DB.get(user_id)["contact_info"]

        return ContactInfo(
            email = user_contacto_info["email"],
            sms = user_contacto_info["sms"],
            prefered_channel = user_contacto_info["prefered_channel"]
         )
    
