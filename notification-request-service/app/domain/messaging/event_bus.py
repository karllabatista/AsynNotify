from abc import ABC,abstractmethod
class EventBus(ABC):
    
    @abstractmethod
    def publish(self):
        pass