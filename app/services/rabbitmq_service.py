import pika
import json
import os
from typing import Dict, Any

# Get connection details from environment variables
# The host MUST be the Docker service name 'rabbitmq'
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "")
RABBITMQ_PASS = os.environ.get("RABBITMQ_PASS", "")

# This queue name will be shared between your API and your OCR worker
OCR_QUEUE_NAME = "ocr_task_queue"


class RabbitMQService:
    """
    A simple, thread-safe service for PUBLISHING messages to RabbitMQ.
    It creates a new connection for each publish, which is a
    robust pattern for web services like FastAPI.
    """

    def __init__(self):
        """Initializes the service with connection parameters."""
        self.credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        self.connection_params = pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=self.credentials
        )
        print("INFO: RabbitMQService initialized.")

    def _get_channel(self):
        """Creates and returns a new connection and channel."""
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        return connection, channel

    def publish_message(self, message: Dict[str, Any], queue_name: str = OCR_QUEUE_NAME):
        """
        Publishes a persistent message to a durable queue.
        """
        connection = None
        try:
            connection, channel = self._get_channel()

            # 1. Declare a DURABLE queue
            # This ensures the queue definition survives a broker restart.
            channel.queue_declare(queue=queue_name, durable=True)

            # 2. Serialize message to JSON
            message_body = json.dumps(message)

            # 3. Publish the message
            channel.basic_publish(
                exchange='',  # Use the default exchange
                routing_key=queue_name,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )  # This ensures the MESSAGE itself is persisted to disk
            )

            print(
                f"SUCCESS: Published message to queue '{queue_name}': {message_body}")
            return True

        except Exception as e:
            print(f"ERROR: Failed to publish message to RabbitMQ: {e}")
            return False
        finally:
            # 4. Always close the connection
            if connection and connection.is_open:
                connection.close()


# --- Create a single, reusable instance for your app ---
# You can import this instance into your other services or routers
rabbitmq_service = RabbitMQService()
