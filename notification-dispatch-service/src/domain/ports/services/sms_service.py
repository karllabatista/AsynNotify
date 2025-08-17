from abc import ABC,abstractmethod

class SMSService(ABC):

    @abstractmethod
    async def send_to_provider(sel,content:dict):
        pass