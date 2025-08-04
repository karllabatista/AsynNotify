from app.domain.repositories.user_repository import UserRepository
class GetContactInfoUseCase:
    
    def __init__(self,repository:UserRepository):
        self.repository = repository

    def execute(self,user_id:str) -> bool:
        self.repository.get_user_by_id(user_id)
        