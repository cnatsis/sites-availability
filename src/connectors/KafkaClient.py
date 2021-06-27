import json

from kafka import KafkaProducer, KafkaConsumer

from src.connectors import AivenConnector
from src.utils import constants

CA_FILE = "certs/cafile"
CERT_FILE = "certs/certfile"
KEY_FILE = "certs/keyfile"


class KafkaClient:
    """
    A class that interacts with Apache Kafka consumers and producers (Aiven Kafka managed service)

    Usage:
    kafka = KafkaClient()
    """

    def __init__(self):
        """
        Initialize KafkaClient.
        """
        super().__init__()
        self.aiven = AivenConnector(constants.config)
        self.kafka = self.aiven.get_service(constants.AIVEN_PROJECT, constants.AIVEN_KAFKA_NAME)
        self.brokers = self.kafka["connection_info"]["kafka"]
        self.create_cert_files()

    def create_consumer(self, group_id, auto_offset_reset) -> KafkaConsumer:
        """
        Creates a Kafka consumer instance
        :param group_id: Group ID
        :param auto_offset_reset: Read from start or end of stream. Valid values 'earliest' or 'latest'.
        :return: KafkaConsumer instance
        :rtype: KafkaConsumer
        """
        return KafkaConsumer(
            bootstrap_servers=self.brokers,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            key_deserializer=lambda m: json.loads(m.decode('utf-8')),
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            security_protocol="SSL",
            ssl_cafile=CA_FILE,
            ssl_certfile=CERT_FILE,
            ssl_keyfile=KEY_FILE
        )

    def create_producer(self) -> KafkaProducer:
        """
        Creates a Kafka producer instance
        :return: KafkaProducer instance
        :rtype: KafkaProducer
        """
        return KafkaProducer(
            bootstrap_servers=self.brokers,
            key_serializer=lambda v: json.dumps(v).encode('utf-8'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            compression_type='gzip',
            security_protocol="SSL",
            ssl_cafile=CA_FILE,
            ssl_certfile=CERT_FILE,
            ssl_keyfile=KEY_FILE
        )

    def produce(self, topic, key, message):
        """
        Method that produces messages to a Kafka topic
        :param topic: Kafka topic
        :param key: Record key
        :param message: record payload
        :return: None
        """
        producer = self.create_producer()
        producer.send(topic, key=key, value=message)

    def create_topic(self,
                     topic,
                     partitions=1,
                     replication=3,
                     min_insync_replicas=2,
                     retention_bytes=-1,
                     retention_hours=168,
                     cleanup_policy='delete'):
        """
        Creates a Kafka topic
        :param topic: topic name
        :param partitions: # of partitions
        :param replication: replication factor
        :param min_insync_replicas: min insync replicas
        :param retention_bytes: retention bytes
        :param retention_hours: retention hours (default: 1 week)
        :param cleanup_policy: cleanup policy (default: delete)
        :return:
        """
        for topic_item in self.kafka["topics"]:
            if topic_item["topic_name"] == topic:
                print(f"Topic {topic} already exists!")
                break
        else:
            print(f"Creating topic {topic}...")
            self.aiven.client.create_service_topic(
                self.aiven.config["project"],
                self.aiven.config["kafka_name"],
                topic,
                partitions,
                replication,
                min_insync_replicas,
                retention_bytes,
                retention_hours,
                cleanup_policy
            )

    def create_cert_files(self):
        """
        Generate certificates
        :return:
        """
        print("Generating cert files...")
        ca = self.aiven.client.get_project_ca(self.aiven.config["project"])
        with open(CA_FILE, "w") as ca_file:
            ca_file.write(ca["certificate"])
        with open(CERT_FILE, "w") as cert_file:
            cert_file.write(self.kafka["connection_info"]["kafka_access_cert"])
        with open(KEY_FILE, "w") as key_file:
            key_file.write(self.kafka["connection_info"]["kafka_access_key"])
