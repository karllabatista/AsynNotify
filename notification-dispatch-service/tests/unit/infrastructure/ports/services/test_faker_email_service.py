from src.infrastructure.ports.services.faker_email_service import FakerEmailService
import pytest

@pytest.mark.asyncio
async def test_faker_email_service_send_success():

    # ARRANGE
    content_mock = {
        "message":" This a message for test",
        "destination": "test@test.com"
    }
    # ASSERT + ACT
    service = FakerEmailService()
    # just checks if it doesn't throw an exception  
    await service.send(content_mock)

