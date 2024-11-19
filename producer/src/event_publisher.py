from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
import json
import os
import time
import logging

topic = os.environ.get('CHANNEL') or 'stats'
batch_size = os.environ.get('BATCH_SIZE') or 16384

linger_ms = os.environ.get('LINGER_MS') or 5
compression_type = os.environ.get('COMPRESSION') or 'gzip'
class Publisher:


    def __init__(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        self.logger = logger

        while not hasattr(self, 'producer'):
            try:
                self.producer = KafkaProducer(bootstrap_servers="kafka:9092",
                                              batch_size = batch_size,
                                              linger_ms = linger_ms,
                                              compression_type = compression_type)
            except NoBrokersAvailable as err:
                self.logger.error("Unable to find a broker: {0}".format(err))
                time.sleep(1)

    def push(self, message):
        self.logger.debug("Publishing: {0}".format(message))
        try:
            if self.producer:
                self.producer.send(topic,
                                   bytes(json.dumps(message).encode('utf-8')))
        except AttributeError:
            self.logger.error("Unable to send {0}. The producer does not exist."
                              .format(message))
            

    """
        Publishes a batch of messages to Kafka.

        Args:
            messages (list): A list of message payloads (strings or bytes).
    """
    def batch_publish(self, messages):
        try:
            for message in messages:
                self.producer.send(self.topic, value=message.encode('utf-8'))
            self.producer.flush()  # Ensure all messages are sent
            print(f"Successfully published {len(messages)} messages to topic {self.topic}")
        except Exception as e:
            print(f"Failed to publish messages: {e}")
        finally:
            self.producer.close()
