from abc import ABC, abstractmethod
class UserContactInfoRepository(ABC):

    @abstractmethod
    def get_contact_info_by_user_id(user_id:str) ->dict:
        pass