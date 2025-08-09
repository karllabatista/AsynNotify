from abc import ABC,abstractmethod
from src.domain.entitites.notification import Notification
class EventBus(ABC):
    

    @abstractmethod
    def consumer_event(self) -> dict:
        pass
