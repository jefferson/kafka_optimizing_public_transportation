"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)

class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = 1
        self.num_replicas = 1

        self.broker_properties = {
            "zookeeper.connect": "localhost:2181",
            "schema.registry.url": "http://localhost:8081",
            "bootstrap.servers": "PLAINTEXT://localhost:9092"
        }

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        self.producer = AvroProducer({
             'bootstrap.servers': self.broker_properties["bootstrap.servers"], 
             'schema.registry.url': self.broker_properties["schema.registry.url"]
        }, default_key_schema=self.key_schema, default_value_schema=self.value_schema)

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""

        client = AdminClient({"bootstrap.servers": self.broker_properties["bootstrap.servers"]})

        new_topic = NewTopic(
            self.topic_name,
            num_partitions=self.num_partitions,
            replication_factor=self.num_replicas,
        )

        future = client.create_topics([new_topic], request_timeout = 30)

        for _, future in future.items():
            try:
                future.result()
                print("Topic {} created".format(_))
            except Exception as identifier:
                print("Failed to create topic {}: {}".format(_, identifier))


    def time_millis(self):
        return int(round(time.time() * 1000))

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""

        self.producer.flush(timeout=10)
        self.producer.close()
        
        logger.info("Code for Producer cleaned")
        return

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
