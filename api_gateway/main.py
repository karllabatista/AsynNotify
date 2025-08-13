from fastapi import FastAPI,Request
import httpx

app = FastAPI()


@app.get("/users/{user_id}/contact-info")
async def get_user_contact_info(user_id:str):
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://127.0.0.1:8001/users/{user_id}/contact-info")

    return resp.json()

@app.post("/notifications")
async def  publish_notification(req:Request):
    """
    curl -X POST -d '{"user_id": "karlla","channel": "email","message": "Você tem uma nova mensagem."}'  http://127.0.0.1:8000/notifications
    
    """
    
    payload = await req.json()
    
    async with httpx.AsyncClient() as client:

        result = await client.post(f"http://127.0.0.1:8002/notifications",json=payload) 
    
    return result.json()