from abc import ABC,abstractmethod

class SMSService(ABC):

    @abstractmethod
    async def send(sel,content:dict):
        pass