from fastapi import APIRouter
import httpx
from clients.user_client import UserClient

base_url = "http://127.0.0.1:8001/"
router = APIRouter()
user_client = UserClient(base_url)

@router.get("/users/{user_id}/contact-info")
async def get_user_contact_info(user_id:str):
 
    return await user_client.get_user_contact_info(user_id)
