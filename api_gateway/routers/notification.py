from fastapi import APIRouter,Request
from clients.notification import Notification

router = APIRouter()

base_url ="http://127.0.0.1:8002" 
notification_client = Notification(base_url)

@router.post("/notifications")
async def  publish_notification_endpoint(req:Request):
    """
    curl -X POST -d '{"user_id": "karlla","channel": "email","message": "Você tem uma nova mensagem."}'  http://127.0.0.1:8000/notifications
    
    """
    payload = await req.json()
        
    return await notification_client.publish_notification(payload)

