from app.domain.repositories.user_contact_info_repository import UserContactInfoRepository
from config.env import get_base_url_user_service
import requests

BASE_URL_USER_SERVICE = get_base_url_user_service()
class UserServiceContactIndoRepository(UserContactInfoRepository):

    def __init__(self,base_url = BASE_URL_USER_SERVICE):
        
        self.base_url = base_url

    def get_contact_info_by_user_id(self,user_id:str) ->dict:
        
        endpoint = f"{self.base_url}/users/{user_id}/contact-info"
        result_data = requests.get(endpoint)
        return result_data.json()