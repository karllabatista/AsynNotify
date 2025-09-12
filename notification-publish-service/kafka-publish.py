from confluent_kafka import Producer
import uuid
import json

conf= {'bootstrap.servers':'localhost:9092'}

producer = Producer(conf)
TOPIC= "notifications"

def delivery_success(err,msg):
    """
    Returns a respose of sucsess or failure
    """

    if err is not  None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else :
        print("Message produced: %s" % (str(msg)))

def send_event (message,user_id):
    producer.produce(TOPIC,key=user_id,value=message,callback=delivery_success)



if __name__ == "__main__":

    user_id = "user_k"

    message ={
        'event_id':str(uuid.uuid4()),
        'event_type':"NOTIFICATION_CREATED",
        "message" :" hello world buddy",
        'user_id':user_id
    }

    payload = json.dumps(message)
    send_event(payload,user_id)

    # forca o envio da mensagem e agaurda a resposta dos callbacks
    producer.flush()