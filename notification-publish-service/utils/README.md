## How to run a Kafka Broker

### How to run Kafka broker without Zookeper

1. Create the cluster id

```bash
docker run --rm confluentinc/cp-kafka:7.5.0 kafka-storage random-uuid

```

2. Copy and paste in the docker-compose file

```docker
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      CLUSTER_ID: 3jnKbaddSwy4g2XwwTQ-5g                                    
```
3. Down any old container

```bash
docker-compose down -v

```
4. Up the container
```bash
docker-compose up -d

```

The result is container with kafka running wit success.

### CREATE A TOPIC

1. Enter into container

```bash
docker exec -it kafka-broker bash
```
2. Typing the command above to create a topic:

```bash
kafka-topics --create --topic notifications --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
Expected output:
```bash
Created topic notifications.

```
### Test producer

```bash
kafka-console-producer --topic notifications --bootstrap-server localhost:9092
```

### Test consumer

```bash
kafka-console-consumer --topic notifications --from-beginning --bootstrap-server localhost:9092
```