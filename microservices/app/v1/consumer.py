import json

import pika
from aio_pika import connect_robust
from core.settings import PUBLISH_QUEUE


class PikaClient:
    """Pika client class, which will handle all the communication with RabbitMQ"""

    def __init__(self, process_callable):
        self.publish_queue_name = PUBLISH_QUEUE
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", heartbeat=600, blocked_connection_timeout=300)
        )
        self.channel = self.connection.channel()
        self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
        self.callback_queue = self.publish_queue.method.queue
        self.response = None
        self.process_callable = process_callable

    async def consume(self, loop):
        """Setup message listener with the current running loop"""

        connection = await connect_robust(host="localhost", port=5672, loop=loop)
        channel = await connection.channel()
        queue = await channel.declare_queue(PUBLISH_QUEUE)
        await queue.purge()
        await queue.consume(callback=self.callback, no_ack=False)
        return connection

    async def callback(self, message):
        """Processing incoming message from RabbitMQ"""

        message.ack()
        body = message.body
        if body:
            self.process_callable(json.loads(body))
