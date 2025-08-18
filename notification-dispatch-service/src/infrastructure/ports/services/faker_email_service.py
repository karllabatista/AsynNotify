from src.domain.ports.services.email_service import EmailService
from src.domain.exceptions.email_service_exception import EmailServiceException
import logging
import asyncio
import random

logger = logging.getLogger(__name__)
class FakerEmailService(EmailService):

 
    async def send_to_provider(self, content:dict) -> dict:

        
        """
        Simulates the async send email by building an EmailMessage
        and logging its content.

        Args:
            content (Dict[str, str]): Dictionary with keys 'destination', 'subject', 'message'.

        Raises:
            ValueError: If mandatory keys are missing in content.
            EmailServiceException: For domain specific email errors.
        """
        logger.debug("Trying to send email through provider..")
        await asyncio.sleep(0.3)

        chance = random.random()

        if chance < 0.7: # [0.0,0.7]: success
            logger.debug("[FakeEmailService]Email sent with success")
            return {
                "status": "sent",
                "message_id": f"msg_{random.randint(1000,9999)}",
                "provider": "FakeEmail",
                "to": content["to"]
            }
        elif chance <0.85: # [0.7,0.85] # temporary error
            logger.error("[FakeEmailService]Email sending failed:Mailbox busy, retry later")
            return {
                "status": "failed",
                "error": "temporary_error",
                "message": "Mailbox busy, retry later"
            }
        elif chance <0.95: # [0.85,0.95]permanent error
            logger.error("[FakeEmailService]Email sending failed:Email address does not exist")
            return {
                "status": "failed",
                "error": "invalid_recipient",
                "message": "Email address does not exist"
            }
        else:  
            logger.error("[FakeEmailService] Email sending failed:Email provider did not respond in time")
            raise TimeoutError("Email provider did not respond in time")



