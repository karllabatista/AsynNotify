from fastapi import FastAPI,Path,Depends,HTTPException
from app.use_cases.get_contact_info_use_case import GetContactInfoUseCase
from app.infrastructure.in_memory_repository import InMemoryRepository
from app.domain.exception.user_not_found_exception import UserNotFoundException
from starlette import status
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def config_use_case():
    repository = InMemoryRepository()
    return GetContactInfoUseCase(repository)

@app.get("/users/{user_id}/contact-info",status_code=status.HTTP_200_OK)
def get_user_contact_info(
    user_id: str = Path(..., min_length=4, max_length=10),
    get_user_contact_info_use_case:GetContactInfoUseCase = Depends(config_use_case)
) :
    try:
      
        contact = get_user_contact_info_use_case.execute(user_id)
        return {"contact_info":contact.to_dict()}
        
    except UserNotFoundException:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message": "user not found"})
    except Exception as e:
        logger.error(f"Unexpected error while fetching user {user_id}: {e}")
        raise HTTPException( status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error")