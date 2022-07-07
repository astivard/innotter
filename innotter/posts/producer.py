from json import dumps

from pika import BlockingConnection, ConnectionParameters

connection = BlockingConnection(ConnectionParameters(host="rabbitmq", heartbeat=600, blocked_connection_timeout=300))

channel = connection.channel()
channel.queue_declare(queue="statistics")


def publish(body) -> None:
    channel.basic_publish(exchange="", routing_key="statistics", body=str.encode(dumps(body)))
