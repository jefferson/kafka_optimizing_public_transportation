from dataclasses import dataclass

@dataclass(frozen=True)
class KafkaEnvoriment:
    boostrap_servers: str = "PLAINTEXT://localhost:9092,PLAINTEXT://localhost:9093,PLAINTEXT://localhost:9094"
    schema_registry_url: str = "http://schema-registry:8081"
    default_partitions: int = 1
    default_replicas: int = 1
    rest_proxy: str = "http://localhost:8082"