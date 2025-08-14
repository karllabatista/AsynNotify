import httpx
class UserClientClientHTTPAsync:

    def __init__(self,base_url):
        
        self.base_url =base_url

    
    async def get_user_contact_info(self,user_id:str):
        
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base_url}/users/{user_id}/contact-info")

        return resp.json()              