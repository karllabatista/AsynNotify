from fastapi import APIRouter
import httpx

router = APIRouter()

@router.get("/users/{user_id}/contact-info")
async def get_user_contact_info(user_id:str):
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://127.0.0.1:8001/users/{user_id}/contact-info")

    return resp.json()              