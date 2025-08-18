from src.domain.ports.dispatchers.channel_dispatcher import ChannelDispatcher
from src.domain.ports.services.sms_service import SMSService
from src.application.services.notification_factory import NotificationFactory
from src.domain.exceptions.channel_dispatcher_error_exception  import ChannelDispatchErrorException
import logging

logger = logging.getLogger(__name__)
class SMSChannelDispatcher(ChannelDispatcher):

    def __init__(self, service:SMSService):
        self.service = service


    async def dispatch(self, notification:NotificationFactory):

        """
        Receive a generic notification,check them and send to Service
        """
        try:
            logger.info(f"[SMS-Dispatcher] Start dispatcher notification to the {notification.channel}")
    
            self._validate_notification(notification)
                
            logger.info (f"[SMS-Dispatcher] Validate mandatory fields OK")
            payload = self._create_payload_sms(notification)
            
            logger.info("[SMS-Dispatcher] Payload created for SMS Service")
            result =  await  self.service.send_to_provider(payload)

            logger.info(f"[SMS-Dispatcher] Notification dispatched successfully: {result}") 
            
            # TODO
            # retries
            # registres failed,success
            if result.get("status") == "sent":
                logger.info("[SMSChannelDispatcher] SMS sent with successfull")
            else:
                logger.info("[SMSChannelDispatcher] error to send sms through provider")
            
                
        except ChannelDispatchErrorException as e:
            logger.error(f"[SMS-Dispatcher] Channel dispatch error: {e}")
            raise

        except Exception as e:
            logger.exception(f"[SMS-Dispatcher] Unexpected error: {e}")
            raise
    
    def _validate_notification(self, notification:NotificationFactory): 
        """
        Validates if mandatory fields are presents
        """
        logger.debug("[SMS-Dispatcher] Validating mandatory fields...")
        if not notification.message or not notification.destination:
            raise ValueError(" Missing mandatory fields")

    
    def _create_payload_sms(self,notification:NotificationFactory):
        """
        Converts the genreci notification to channel format
        """
        logger.debug("[SMS-Dispatcher] Converting notification to SMS payload")
        return {
            "message": notification.message,
            "to": notification.destination  

        }