import os
from json import dumps, loads
from kafka import KafkaConsumer, KafkaProducer


class KafkaProvider:
    def __init__(self, config):
        self.__config = config

    def producer(self):
        return KafkaProducer(
            bootstrap_servers=self.get_brokers().split(","),
            value_serializer=lambda x: dumps(x).encode('utf-8'))

    def consumer(self):
        return KafkaConsumer(
            bootstrap_servers=self.get_brokers().split(","),
            value_deserializer=lambda x: loads(x.decode('utf-8')))

    def get_brokers(self):
        kafkaBrokers = os.environ['KAFKA_TOPIC_SWORDPHISH3']
        return kafkaBrokers
