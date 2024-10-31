
import time

from mq_connector import RabbitMQClient

# read rabbitmq connection url from environment variable
client = RabbitMQClient(queue_name='test')


client.consume_message()
