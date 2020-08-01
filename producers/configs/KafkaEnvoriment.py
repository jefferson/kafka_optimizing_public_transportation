from dataclasses import dataclass

@dataclass(frozen=True)
class KafkaEnvoriment:
    boostrap_servers: str = "PLAINTEXT://localhost:9092,PLAINTEXT://localhost:9093,PLAINTEXT://localhost:9094"
    schema_registry_url: str = "http://schema-registry:8081"
    default_partitions: int = 1
    default_replicas: int = 1
    rest_proxy: str = "http://rest-proxy:8082/"
    kafka_conector_url: str = "http://kafka-connect:8083/connectors"
    kafka_conector_name: str = "stations"
    database_url: str = "jdbc:postgresql://postgres:5432/cta"
    database_user: str = "cta_admin"
    database_password: str = "chicago"