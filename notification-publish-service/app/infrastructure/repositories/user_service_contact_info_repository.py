from app.domain.repositories.user_contact_info_repository import UserContactInfoRepository
from app.domain.entities.contact_info import ContactInfo
from app.domain.exceptions.external_server_exception import ExternalServiceException
from app.domain.exceptions.user_not_found_exception import UserNotFound
import requests
from requests.exceptions import RequestException
import logging

logger = logging.getLogger(__name__)


class UserServiceContactIndoRepository(UserContactInfoRepository):

    def __init__(self,base_url:str):
        
        self.base_url = base_url

    def get_contact_info_by_user_id(self,user_id:str) ->ContactInfo:
        
        try:
        
            endpoint = f"{self.base_url}/users/{user_id}/contact-info"
            result = requests.get(endpoint,timeout=5)

            if result.status_code == 404:
                raise UserNotFound ("User not found")

            if result.status_code != 200:
                logger.error(f"Failed to get user contact info to user {user_id}")
                raise ExternalServiceException(f"Failed to get user contact info to user {user_id}")
            
            data = result.json()

            required_fields = ["email","sms","preferred_channel"]

            if not all(field in data for field in required_fields):
                raise ExternalServiceException("Incomplete user data from user service")

            return ContactInfo(email=data["email"],
                            sms=data["sms"],
                            preferred_channel=data["preferred_channel"])
        except RequestException as e:
            logger.error(f"Request to user service failed: {e}")
            raise ExternalServiceException("Could not reach user service")

        except UserNotFound:
            raise
        except ExternalServiceException:
            raise
        except Exception as e:
            logger.exception(f"An unexpected error in calling to user service:{e}")
            raise
