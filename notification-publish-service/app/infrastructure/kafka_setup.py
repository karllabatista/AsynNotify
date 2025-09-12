from confluent_kafka import Producer
from config.env  import get_kafka_port,get_kafka_server

def initiacializa_kafka():
    
    SERVER = get_kafka_server()
    PORT = get_kafka_port()
    conf = {"bootstrap.servers": f"{SERVER}:{PORT}"}
    return conf

def create_producer():
    conf = initiacializa_kafka()
    return Producer(conf)

