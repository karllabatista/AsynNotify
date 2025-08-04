from abc import ABC,abstractmethod
from app.domain.entities.contact_info import ContactInfo
class UserRepository(ABC):
    
    @abstractmethod
    def get_user_by_id(self,user_id:str) -> ContactInfo:
        pass