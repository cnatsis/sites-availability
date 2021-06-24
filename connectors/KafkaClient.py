import json

from kafka import KafkaProducer, KafkaConsumer
from connectors import PostgreSQLConnector

from utils import constants


class KafkaClient:
    """
    Usage:
    kafka = KafkaClient('localhost', 9092)
    """

    def __init__(self, bootstrap_servers='localhost:9092'):
        """
        Initialize KafkaClient.
        :param broker: Kafka broker IP
        :param port: Kafka broker port (default: 9092)
        """
        super().__init__()
        self.kafka = None
        self.brokers = bootstrap_servers

    def create_consumer(self, group_id, auto_offset_reset) -> KafkaConsumer:
        return KafkaConsumer(
            bootstrap_servers=self.brokers,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            key_deserializer=lambda m: json.loads(m.decode('utf-8')),
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            # security_protocol="SSL",
            # ssl_cafile=constants.CA_FILE,
            # ssl_certfile=constants.CERT_FILE,
            # ssl_keyfile=constants.KEY_FILE
        )

    def create_producer(self) -> KafkaProducer:
        return KafkaProducer(
            bootstrap_servers=self.brokers,
            key_serializer=lambda v: json.dumps(v).encode('utf-8'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            compression_type='gzip'
            # security_protocol="SSL",
            # ssl_cafile=ca_path,
            # ssl_certfile=cert_path,
            # ssl_keyfile=key_path,
        )

    def consume(self, topics, group_id, auto_offset_reset, pg_table):
        consumer = self.create_consumer(group_id, auto_offset_reset)
        print("Consuming Kafka Topic. Press Ctrl+C to exit")
        consumer.subscribe(topics)
        # Group rebalancing !!!!!!

        con = PostgreSQLConnector("localhost", 5432, "sites", "postgres", "postgres")

        try:
            for msg in consumer:
                # print(msg)
                print(f"Topic: {msg.topic}, Offset: {msg.offset}, Key: {msg.key}, Value: {msg.value}")
                con.insert(pg_table, msg.value)
            con.close()
        except KeyboardInterrupt:
            consumer.commit()
            consumer.close()
            con.close()

    def produce(self, topic, key, message):
        producer = self.create_producer()
        producer.send(topic, key=key, value=message)
