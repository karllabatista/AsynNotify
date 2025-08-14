from fastapi import APIRouter
from api_gateway.clients.user_client_htpp import UserClientClientHTTPAsync

base_url = "http://127.0.0.1:8001"
router = APIRouter()
user_client = UserClientClientHTTPAsync(base_url)

@router.get("/users/{user_id}/contact-info")
async def get_user_contact_info_endpoint(user_id:str):
 
    return await user_client.get_user_contact_info(user_id)
