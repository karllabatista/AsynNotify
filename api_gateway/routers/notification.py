from fastapi import APIRouter,Request
import httpx

router = APIRouter()

@router.post("/notifications")
async def  publish_notification(req:Request):
    """
    curl -X POST -d '{"user_id": "karlla","channel": "email","message": "Você tem uma nova mensagem."}'  http://127.0.0.1:8000/notifications
    
    """
    
    payload = await req.json()
    
    async with httpx.AsyncClient() as client:

        result = await client.post(f"http://127.0.0.1:8002/notifications",json=payload) 
    
    return result.json()