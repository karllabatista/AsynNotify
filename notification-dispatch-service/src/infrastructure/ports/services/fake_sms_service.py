from src.domain.ports.services.sms_service import SMSService
import logging
import asyncio
import random

logger = logging.getLogger(__name__)

class FakeSMSService(SMSService):
    
    async def send_to_provider(sel, content:dict) -> dict:
        """
        Simulates the sms send for a provider.
        Returns
        """
        logger.debug("[FAKERSMSSERVICE] Trying send sms through provider ..")
        await asyncio.sleep(0.2) ## simlualtes network latency
        

        if random.random() < 0.3:
            logger.error("[FAKERSMSSERVICE] error to send sms through provider ..")
            return {

            "status":"failed",
            "provider_message_id": None,
            "error": "Simulated provider error"
        }

        logger.debug("[FAKERSMSSERVICE] SMS sent with successfull")
        return {

            "status":"sent",
            "provider-mensage-id":f"faker-{random.randint(1000,9999)}",
            "to": content.get("to"),
            "message":content.get("message")
        }
        