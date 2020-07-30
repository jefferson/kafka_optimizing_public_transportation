"""Producer base-class providing common utilites and functionality"""
import logging
import time


from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)

from configs.KafkaEnvoriment import KafkaEnvoriment

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
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        self.broker_properties = {
            "bootstrap.servers": KafkaEnvoriment.boostrap_servers,
            "schema.registry.url": KafkaEnvoriment.schema_registry_url
        }

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        self.producer = AvroProducer(
            self.broker_properties,
            default_key_schema  = self.key_schema,
            default_value_schema  = self.value_schema
        )

    def create_topic(self):
        """Creates the producer topic if it does not already exist"""

        client = AdminClient({"bootstrap.servers": self.broker_properties["boostrap.servers"]})

        new_topic = [NewTopic(
            self.topic_name,
            num_partitions=self.num_partitions,
            replication_factor=self.num_replicas
        )]

        future = client.create_topic(new_topic)

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
        #
        #
        # TODO: Write cleanup code for the Producer here
        #
        #
        
        logger.info("There is nothing to do here")

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
