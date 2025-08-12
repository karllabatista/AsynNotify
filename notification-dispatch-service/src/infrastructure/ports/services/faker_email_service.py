from src.domain.ports.services.email_service import EmailService
from src.domain.exceptions.email_service_exception import EmailServiceException
import logging
import asyncio
from email.message import EmailMessage
from typing import Dict

logger = logging.getLogger(__name__)
class FakerEmailService(EmailService):

    def __init__(self):
        self.last_email = ""


    async def send(self, content:dict):

        
        """
        Simulates the async send email by building an EmailMessage
        and logging its content.

        Args:
            content (Dict[str, str]): Dictionary with keys 'destination', 'subject', 'message'.

        Raises:
            ValueError: If mandatory keys are missing in content.
            EmailServiceException: For domain specific email errors.
        """
        
        try:
            self._validate_input(content)
            # guarantee send stateless and independent
            msg = EmailMessage()
            msg["Subject"] = content.get('subject','No subject')
            msg["From"] = 'study@studycloud.com.br'
            msg["To"] = content.get('destination','unknown@example.com')


            body = content.get('message') or ''
            msg.set_content(body)

            logger.info(f"[FAKE EMAIL SERVICE SENT] EMAIL to: {msg['To']}")
            self.last_email = {"destination":msg["To"]}

            logger.debug(f"Subject: {msg['Subject']}")
            logger.debug(f"Email content:\n{msg.as_string()}")

            await asyncio.sleep(0.5)
        except EmailServiceException as e:
            logger.error(f"[FAKE EMAIL SERVICE ERROR] Failed to send email:{e}")
            raise
        except Exception as e:
            logger.exception(f"[FAKE EMAIL SERVICE ERROR] An error occorred when send email:{e}")
            raise

    def _validate_input(self,content:Dict[str,str]) -> None:

        if not content.get('message') or not content.get('destination'):
            raise ValueError("Missing mandatory keys 'message' or 'destination'")