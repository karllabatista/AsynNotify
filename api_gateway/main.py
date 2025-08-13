from fastapi import FastAPI
from starlette import status
import httpx
app = FastAPI()


@app.get("/users/{user_id}/contact-info",status_code=status.HTTP_200_OK)
async def get_user_contact_info(user_id:str):
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://127.0.0.1:8001/users/{user_id}/contact-info")

    return resp.json()
