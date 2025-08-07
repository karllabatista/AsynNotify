from abc import ABC,abstractmethod
from app.domain.entitites.notification import Notification
class ChannelDispatcher(ABC):
    
    @abstractmethod
    def dispatch(self, notification: Notification) -> None:
        pass