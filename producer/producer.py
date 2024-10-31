
import os
from mq_connector import RabbitMQClient

# read rabbitmq connection url from environment variable
client = RabbitMQClient(queue_name='test')

print("get the connection")
# publish a 100 messages to the queue
for i in range(100):
    client.publish_message("publishing test")

# close the channel and connection
# to avoid program from entering with any lingering
# message in the queue cache
print("sending message over")
client.close_connection()