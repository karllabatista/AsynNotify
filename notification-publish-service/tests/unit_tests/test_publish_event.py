from unittest.mock import Mock
from app.infrastructure.messaging.in_memory_event_bus import InMemoryEventBus
def test_publish_event():

    # arrange
    event= Mock()

    event.to_dict.return_value = {"user_id": "123", "message": "Hello"}

    # ACT
    inmemory_queue = InMemoryEventBus()
    success =   inmemory_queue.publish(event)

    # ASSERT
    assert success is True