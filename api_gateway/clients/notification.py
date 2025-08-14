from fastapi import Request
import httpx
class Notification:

    def __init__(self,base_url):
        self.base_url = base_url

    
    async def publish_notification(self,payload):
        """
        curl -X POST -d '{"user_id": "karlla","channel": "email","message": "Você tem uma nova mensagem."}'  http://127.0.0.1:8000/notifications
        
        """
        
        async with httpx.AsyncClient() as client:

            result = await client.post(f"{self.base_url}/notifications",json=payload) 
        
        return result.json()