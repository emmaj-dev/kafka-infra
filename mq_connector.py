import pika
import os
import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

class RabbitMQClient:
    def __init__(self, queue_name='default_queue'):
        # Retrieve the AMQP URL from environment variables
        amqp_url = os.environ.get('AMQP_URL')
        if not amqp_url:
            raise ValueError("AMQP_URL environment variable is not set.")
        
        try: 
            url_params = pika.URLParameters(amqp_url)
            self.queue_name = queue_name

            # Establish the connection with the URL parameters
            self.connection = pika.BlockingConnection(url_params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            # sys.exit(1)


    def publish_message(self, message: str):
        """Publish a message to the specified RabbitMQ queue."""
        try: 
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
            )
            logger.info(f" [x] Sent '{message}'")
        except Exception as e:
            logger.error(f"publish failed: {e}")

        

    def consume_message(self):
        """Consume messages from the specified RabbitMQ queue."""
        try:
            def callback(ch, method, properties, body):
                logging.info(f" [x] Received '{body.decode()}'")
                # Acknowledge the message after processing
                ch.basic_ack(delivery_tag=method.delivery_tag)

            logger.info(f" [*] Waiting for messages in {self.queue_name}. To exit, press CTRL+C")
            self.channel.basic_qos(prefetch_count=1)  # Fair dispatch
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
            self.channel.start_consuming()
        except Exception as e:
            logger.error(f"consume failed: {e}")

    def close_connection(self):
        """Close the RabbitMQ connection."""
        if self.connection:
            self.channel.close()
            self.connection.close()
            logger.info("RabbitMQ connection closed")