from fastapi import APIRouter,Request
from app.clients.notification_client_http import NotificationClientHTTPAsync
from app.config.env import get_base_url_publish_notitication_service
router = APIRouter()

base_url =get_base_url_publish_notitication_service() 
notification_client = NotificationClientHTTPAsync(base_url)

@router.post("/notifications")
async def  publish_notification_endpoint(req:Request):
    """
    curl -X POST -d '{"user_id": "karlla","channel": "email","message": "Você tem uma nova mensagem."}'  http://127.0.0.1:8000/notifications
    
    """
    payload = await req.json()
        
    return await notification_client.publish_notification(payload)

