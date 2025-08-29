from app.domain.ports.event_bus import EventBus
from app.domain.events.notification_event import NotificationEvent
from app.domain.exceptions.event_bus_exceptions import EventBusPermanentError,EventBusTemporaryError,EventBusError
from config.env import get_kafka_topic_name
import json
import logging
from confluent_kafka.error import ProduceError,KafkaException

logger= logging.getLogger(__name__)

TOPIC = get_kafka_topic_name()

class KafkaEventBus(EventBus):
    
    def __init__(self,conf:dict,producer):
        self.conf=  conf
        self.producer= producer

    def publish(self,event:NotificationEvent):
   
        """
        Publish a event in Kafka Broker
        """

        logger.info("[Kafka Producer] Trying to pushing event in Kafka broker")
        try:
            key = event.user_id
            payload= json.dumps(event.to_dict())
            self.producer.produce(TOPIC, key=key, value=payload,callback=self._delivery_report)
            self.producer.flush(timeout=5)  # guarantee send

        except BufferError as error:
            logger.error(f"[Kafka Producer] buffer is full:{error}")
            raise EventBusTemporaryError("Kafka buffer full") from error
        
        except ValueError as error:
            logger.error(f"[Kafka Producer] Invalid payload! {error}")
            raise EventBusPermanentError("Invalid payload") from error
        
        except (ProduceError,KafkaException) as error:
            logger.error(f"[Kafka Producer] Error to produce event:{error}")
            raise EventBusTemporaryError("Kafka internal error") from error
        
        except Exception as error:
            logger.error(f"[Kafka Producer] An error occurred when trying publish event:{error}")
            raise EventBusError("Unexpected error in KafkaEventBus") from error
    
    def _delivery_report(self,err,msg):
            """
            Send an ACK to confirm success or failed of delivery message
            """
        
            if err is not None:
                logger.error(f"Failed to deliver message: %s: %s" % (str(msg), str(err)))
            else:
                logger.info(f"Message produced: %s" % (str(msg)))

    
       