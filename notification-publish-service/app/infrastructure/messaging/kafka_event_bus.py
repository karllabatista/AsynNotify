from app.domain.ports.event_bus import EventBus
from app.domain.events.notification_event import NotificationEvent
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

    def publish(self,event:NotificationEvent)->bool:
   
        """
        Publish a event in Kafka Broker
        """

        logger.info("[Kafka Producer] Trying to pushing event in Kafka broker")
        try:
            key = event.user_id
            payload= json.dumps(event.to_dict())
            self.producer.produce(TOPIC, key=key, value=payload,callback=self._delivery_report)
            self.producer.flush()  # guarantee send

            return True

        except BufferError as error:
            logger.error(f"[Kafka Producer] buffer is full:{error}")
            return False
        
        except ValueError as error:
            logger.error(f"[Kafka Producer] Invalid payload! {error}")
            return False
        
        except ProduceError as error:
            logger.error(f"[Kafka Producer] Error to produce event:{error}")
            return False
        
        except KafkaException as error:
            logger.error(f"[Kafka Producer] Kakfka internal error:{error}")
            return False
        
        except Exception as error:
            logger.error(f"[Kafka Producer] An error occurred when trying publish event:{error}")
            return False
    
    def _delivery_report(self,err,msg):
            """
            Send an ACK to confirm success or failed of delivery message
            """
        
            if err is not None:
                logger.error(f"Failed to deliver message: %s: %s" % (str(msg), str(err)))
            else:
                logger.info(f"Message produced: %s" % (str(msg)))

    
       