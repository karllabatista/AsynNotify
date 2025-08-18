from abc import ABC,abstractmethod


class EmailService(ABC):

    @abstractmethod
    async def send_to_provider(self,content: dict) -> None:
        pass