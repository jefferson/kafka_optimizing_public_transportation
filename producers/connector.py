"""Configures a Kafka Connector for Postgres Station data"""
import json
import logging

import requests

from configs.KafkaEnvoriment import KafkaEnvoriment

logger = logging.getLogger(__name__)

KAFKA_CONNECT_URL = KafkaEnvoriment.kafka_conector_url

CONNECTOR_NAME = KafkaEnvoriment.kafka_conector_name

def configure_connector():
    """Starts and configures the Kafka Connect connector"""
    logging.debug("creating or updating kafka connect connector...")

    resp = requests.get(f"{KAFKA_CONNECT_URL}/{CONNECTOR_NAME}")

    if resp.status_code == 200:
        logging.debug("connector already created skipping recreation")
        return

    data = json.dumps({
           "name": CONNECTOR_NAME,
           "config": {
               "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
               "key.converter": "org.apache.kafka.connect.json.JsonConverter",
               "key.converter.schemas.enable": "false",
               "value.converter": "org.apache.kafka.connect.json.JsonConverter",
               "value.converter.schemas.enable": "false",
               "batch.max.rows": "500",
               # TODO
               "connection.url": f"{KafkaEnvoriment.database_url}",
               # TODO
               "connection.user": f"{KafkaEnvoriment.database_user}",
               # TODO
               "connection.password": f"{KafkaEnvoriment.database_password}",
               # TODO
               "table.whitelist": "stations",
               # TODO
               "mode": "incrementing",
               # TODO
               "incrementing.column.name": "stop_id",
               # TODO
               "topic.prefix": "jdbc.postgres.",
               # TODO
               "poll.interval.ms": "60000",
           }
       })

    print(data)
    # TODO: Complete the Kafka Connect Config below.
    # Directions: Use the JDBC Source Connector to connect to Postgres. Load the `stations` table
    # using incrementing mode, with `stop_id` as the incrementing column name.
    # Make sure to think about what an appropriate topic prefix would be, and how frequently Kafka
    # Connect should run this connector (hint: not very often!)
    logger.info("connector code not completed!")
    resp = requests.post(
       KAFKA_CONNECT_URL,
       headers={"Content-Type": "application/json"},
       data=data,
    )

    ## Ensure a healthy response was given
    resp.raise_for_status()
    logging.debug("connector created successfully")


if __name__ == "__main__":
    configure_connector()
