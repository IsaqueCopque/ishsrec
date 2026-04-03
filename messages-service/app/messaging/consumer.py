import json
import logging
import os
import threading
import time

import pika
from app.services import DeviceRecordService

LOG = logging.getLogger(__name__)

EXCHANGE_NAME= "amq.topic"
QUEUE_NAME = "devices_queue"
ROUTING_KEY= "home.devices"

class RabbitConsumer:

    def __init__(self):
        self.service = DeviceRecordService()

    """Returns rabbitMq connections parameters"""
    def _get_connection_params(self):
        credentials = pika.PlainCredentials(
            os.environ.get("RABBITMQ_DEFAULT_USER", "ishsrec"),
            os.environ.get("RABBITMQ_DEFAULT_PASS", "ishsrec"))
        return pika.ConnectionParameters(
            host= os.environ.get("RABBITMQ_HOST", "rabbitmq"),
            port= int(os.environ.get("RABBITMQ_AMQP_PORT", "5672")),
            credentials= credentials,
            heartbeat=600,
            blocked_connection_timeout=300,
        )

    def _on_device_message(self, channel, method, properties, body):
        try:
            data = json.loads(body)
            self.service.create_device_record(data)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        except (json.JSONDecodeError) as e:
            LOG.warning("--> Consumer: Invalid device message, rejecting: %s", e)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        except Exception as e:
            LOG.exception("--> Consumer: Error processing device message: %s", e)
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


    def _run_device_message_consumer(self):
        while True:
            connection = None
            try:
                params = self._get_connection_params()
                connection = pika.BlockingConnection(params)
                channel = connection.channel()
                channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)
                channel.queue_declare(queue=QUEUE_NAME, durable=True)
                channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(
                    queue=QUEUE_NAME,
                    on_message_callback=self._on_device_message,
                )
                LOG.info("--> Consumer: Consuming from %s", QUEUE_NAME)
                channel.start_consuming()
            except pika.exceptions.AMQPConnectionError as e:
                LOG.warning("--> Consumer: RabbitMQ connection failed, retrying: %s", e)
            except Exception as e:
                LOG.exception("--> Consumer: Consumer error: %s", e)
            finally:
                try:
                    if connection and connection.is_open:
                        connection.close()
                except Exception:
                    LOG.warning("Error closing RabbitMQ connection")
            time.sleep(10)

    """Start a consumer in daemon thread to consume device messages."""
    def start_consumer(self):
        consumer_thread = threading.Thread(target=self._run_device_message_consumer, daemon=True)
        consumer_thread.start()
        return consumer_thread
