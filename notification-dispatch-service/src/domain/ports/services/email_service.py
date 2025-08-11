from abc import ABC,abstractmethod


class EmailService(ABC):

    @abstractmethod
    async def send(self,content: dict) -> None:
        pass