from abc import ABC,abstractmethod
from app.domain.entitites.notification import Notification
class EventBus(ABC):
    

    @abstractmethod
    def consumer(event:dict) -> Notification :
        pass
