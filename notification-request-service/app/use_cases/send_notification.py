from app.domain.messaging.event_bus import EventBus

class SendNotificationUseCase:
    def __init__(self,event_bus:EventBus):
        self.event_bus = event_bus

    def execute(self,event:dict) -> None:

        self.event_bus.publish(event)