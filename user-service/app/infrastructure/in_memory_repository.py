from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.contact_info import ContactInfo 
from app.domain.exception.user_not_found_exception import UserNotFoundException
from app.domain.exception.contact_info_exception import ContactInfoException
import logging

logger = logging.getLogger(__name__)

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

        try:

            if not user_id:
                raise ValueError(" The user_id can`t be none")
            
            logger.info(f"[USERSERVICE] Find user {user_id} .. ")
            user_data= InMemoryRepository.USER_DB.get(user_id)

            if user_data is None:
                logger.warning(f"[USERSERVICE] User with ID '{user_id}' not found.")
                raise UserNotFoundException(f"User with ID '{user_id}' not found.")

            user_contact_info = user_data["contact_info"]
            logger.info(f"[USERSERVICE] Returning contact info from {user_id}")
            return ContactInfo(
                email = user_contact_info["email"],
                sms = user_contact_info["sms"],
                prefered_channel = user_contact_info["prefered_channel"]
            )
        except UserNotFoundException:
            raise
        except Exception as error:
            logger.exception(f"[USERSERVICE] Failed while searching for user with {user_id}:{error}")
            raise ContactInfoException(f"Inernal error while searching for user with {user_id}") from error

