from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.contact_info import ContactInfo
class GetContactInfoUseCase:
    
    def __init__(self,repository:UserRepository):
        self.repository = repository

    def execute(self,user_id:str) -> ContactInfo:
        return self.repository.get_user_by_id(user_id)
        