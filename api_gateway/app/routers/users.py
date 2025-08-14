from fastapi import APIRouter
from app.clients.user_client_htpp import UserClientClientHTTPAsync
from app.config.env import get_base_url_user_service

base_url = get_base_url_user_service()
router = APIRouter()
user_client = UserClientClientHTTPAsync(base_url)

@router.get("/users/{user_id}/contact-info")
async def get_user_contact_info_endpoint(user_id:str):
 
    return await user_client.get_user_contact_info(user_id)
